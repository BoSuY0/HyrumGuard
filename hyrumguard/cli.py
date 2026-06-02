from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path
from typing import Any

from hyrumguard.analysis import analyze_risks
from hyrumguard.canary import plan_canary
from hyrumguard.config import load_config, starter_config_text
from hyrumguard.diff import git_diff, parse_unified_diff
from hyrumguard.discovery import discover_dependents, parse_seed
from hyrumguard.io import read_json, write_json, write_text
from hyrumguard.miners import mine_repository
from hyrumguard.reporters import render_json, render_markdown, render_sarif
from hyrumguard.synthesis import synthesize_contracts
from hyrumguard.validation import (
    ValidationError,
    load_artifact,
    validate_config,
    validate_dependents,
    validate_lockfile,
    validate_risks,
    validate_sarif,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hyrumguard",
        description="HyrumGuard mines downstream usage into shadow contracts and reports PR-time implicit compatibility risk.",
    )
    parser.add_argument("--debug", action="store_true", help="show Python tracebacks for HyrumGuard internal errors")
    subparsers = parser.add_subparsers(dest="command")

    init = subparsers.add_parser("init", help="write a starter HyrumGuard config")
    init.add_argument("--path", default=".hyrumguard.yml", help="config path to write")
    init.add_argument("--overwrite", action="store_true", help="replace an existing config file")
    init.set_defaults(func=cmd_init)

    discover = subparsers.add_parser("discover", help="discover or record downstream dependent repositories")
    discover.add_argument("target", help="target package or repository name")
    discover.add_argument("--ecosystems", default="pypi,npm", help="comma-separated ecosystem names")
    discover.add_argument("--top", type=int, default=40)
    discover.add_argument("--seed", action="append", default=[], help="manual seed as name=path or path")
    discover.add_argument("--config")
    discover.add_argument("--mailto")
    discover.add_argument("--out", default=".hyrum/dependents.json")
    discover.set_defaults(func=cmd_discover)

    infer = subparsers.add_parser("infer", help="infer shadow contracts from dependent repositories")
    infer.add_argument("--from", dest="from_path", required=True, help="dependents JSON file")
    infer.add_argument("--out", default=".hyrum/shadow-contracts.lock.json")
    infer.add_argument("--target-package", help="override target package for all dependents")
    infer.add_argument("--confidence-threshold", type=float, default=0.7)
    infer.set_defaults(func=cmd_infer)

    check = subparsers.add_parser("check", help="match a PR diff against shadow contracts")
    check.add_argument("--contracts", default=".hyrum/shadow-contracts.lock.json")
    check.add_argument("--base")
    check.add_argument("--head")
    check.add_argument("--diff-file")
    check.add_argument("--config")
    check.add_argument("--out", default=".hyrum/risks.json")
    check.set_defaults(func=cmd_check)

    canary = subparsers.add_parser("canary", help="plan or execute changed-only downstream canaries")
    canary.add_argument("--risks", default=".hyrum/risks.json")
    canary.add_argument("--dependents", default=".hyrum/dependents.json")
    canary.add_argument("--affected-only", action="store_true")
    canary.add_argument("--max-repos", type=int, default=8)
    canary.add_argument("--execute", action="store_true")
    canary.add_argument(
        "--allow-unsafe-execution",
        action="store_true",
        help="acknowledge that executing downstream code is unsafe without an external sandbox",
    )
    canary.add_argument("--timeout-seconds", type=int, default=300)
    canary.add_argument("--out", default=".hyrum/canary.json")
    canary.set_defaults(func=cmd_canary)

    report = subparsers.add_parser("report", help="render risk output as JSON, Markdown, or SARIF")
    report.add_argument("--risks", default=".hyrum/risks.json")
    report.add_argument("--format", choices=["json", "markdown", "sarif"], required=True)
    report.add_argument("--out")
    report.set_defaults(func=cmd_report)

    validate = subparsers.add_parser("validate", help="validate HyrumGuard config and artifact files")
    validate.add_argument("--config")
    validate.add_argument("--dependents")
    validate.add_argument("--contracts")
    validate.add_argument("--risks")
    validate.add_argument("--sarif")
    validate.set_defaults(func=cmd_validate)

    return parser


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.path)
    if target.exists() and not args.overwrite:
        raise ValidationError(f"config already exists: {target}; pass --overwrite to replace it")
    write_text(target, starter_config_text())
    print(f"wrote starter config to {target}")
    return 0


def cmd_discover(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    if config:
        validate_config(config)
    discovery_config = config.get("discovery", {})
    seeds = []
    for seed in discovery_config.get("seeds", []):
        seeds.append(parse_seed(seed) if isinstance(seed, str) else seed)
    seeds.extend(parse_seed(seed) for seed in args.seed)
    configured_ecosystems = discovery_config.get("ecosystems")
    if isinstance(configured_ecosystems, str):
        ecosystems = [item.strip() for item in configured_ecosystems.split(",") if item.strip()]
    elif configured_ecosystems:
        ecosystems = [str(item).strip() for item in configured_ecosystems if str(item).strip()]
    else:
        ecosystems = [item.strip() for item in args.ecosystems.split(",") if item.strip()]
    package = config.get("target", {}).get("package") or args.target
    payload = discover_dependents(package, ecosystems, args.top, seeds, args.mailto)
    write_json(args.out, payload)
    print(f"wrote {len(payload['dependents'])} dependents to {args.out}")
    return 0


def cmd_infer(args: argparse.Namespace) -> int:
    payload = read_json(args.from_path)
    atoms = []
    for dependent in payload.get("dependents", []):
        path = dependent.get("path")
        if not path:
            continue
        target_package = args.target_package or dependent.get("target_package") or payload.get("target", {}).get("package")
        if not target_package:
            raise ValueError(f"Dependent {dependent.get('name', path)} has no target_package")
        atoms.extend(mine_repository(path, target_package=target_package, dependent=dependent.get("name")))
    lockfile = synthesize_contracts(atoms, confidence_threshold=args.confidence_threshold)
    write_json(args.out, lockfile)
    print(f"wrote {len(lockfile['contracts'])} shadow contracts to {args.out}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    lockfile = read_json(args.contracts)
    config = load_config(args.config)
    if config:
        validate_config(config)
    if args.diff_file:
        diff = parse_unified_diff(Path(args.diff_file).read_text())
    else:
        diff = git_diff(args.base, args.head)
    risks = analyze_risks(lockfile, diff, suppressions=config.get("suppressions", []))
    write_json(args.out, risks)
    print(f"wrote {risks['summary']['risk_count']} risks to {args.out}")
    return 0


def cmd_canary(args: argparse.Namespace) -> int:
    if args.execute and not args.allow_unsafe_execution:
        raise ValidationError("canary --execute requires --allow-unsafe-execution")
    risks = read_json(args.risks)
    dependents_payload = read_json(args.dependents)
    payload = plan_canary(
        risks,
        dependents_payload.get("dependents", []),
        affected_only=args.affected_only,
        max_repos=args.max_repos,
        execute=args.execute,
        timeout_seconds=args.timeout_seconds,
    )
    write_json(args.out, payload)
    print(f"wrote canary {payload['mode']} for {len(payload['selected'])} dependents to {args.out}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    risks = read_json(args.risks)
    rendered = _render(args.format, risks)
    if args.out:
        write_text(args.out, rendered)
        print(f"wrote {args.format} report to {args.out}")
    else:
        print(rendered, end="")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    artifact_count = 0
    if args.config:
        validate_config(load_config(args.config))
        artifact_count += 1
    if args.dependents:
        validate_dependents(load_artifact(args.dependents))
        artifact_count += 1
    if args.contracts:
        validate_lockfile(load_artifact(args.contracts))
        artifact_count += 1
    if args.risks:
        validate_risks(load_artifact(args.risks))
        artifact_count += 1
    if args.sarif:
        validate_sarif(load_artifact(args.sarif))
        artifact_count += 1
    if artifact_count == 0:
        raise ValidationError("no artifacts selected; pass at least one --config, --dependents, --contracts, --risks, or --sarif")
    print(f"validated {artifact_count} artifact(s)")
    return 0


def _render(format_name: str, risks: dict[str, Any]) -> str:
    if format_name == "json":
        return render_json(risks)
    if format_name == "markdown":
        return render_markdown(risks)
    if format_name == "sarif":
        return render_sarif(risks)
    raise ValueError(format_name)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except Exception as exc:
        if getattr(args, "debug", False):
            traceback.print_exc()
        else:
            print(f"hyrumguard: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
