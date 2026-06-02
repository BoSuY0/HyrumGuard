from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from hyrumguard import __version__
from hyrumguard.config import load_config
from hyrumguard.validation import (
    load_artifact,
    validate_config,
    validate_dependents,
    validate_lockfile,
    validate_risks,
    validate_sarif,
)


Validator = Callable[[Any], None]


def build_doctor_payload(
    config: str | Path | None = None,
    dependents: str | Path | None = None,
    contracts: str | Path | None = None,
    risks: str | Path | None = None,
    sarif: str | Path | None = None,
) -> dict[str, Any]:
    checks = [_passed("package", None, f"HyrumGuard {__version__} importable")]
    if config:
        checks.append(_check_config(config))
    if dependents:
        checks.append(_check_artifact("dependents", dependents, validate_dependents))
    if contracts:
        checks.append(_check_artifact("contracts", contracts, validate_lockfile))
    if risks:
        checks.append(_check_artifact("risks", risks, validate_risks))
    if sarif:
        checks.append(_check_artifact("sarif", sarif, validate_sarif))

    failed = sum(1 for check in checks if check["status"] == "failed")
    passed = sum(1 for check in checks if check["status"] == "passed")
    return {
        "schema_version": 1,
        "summary": {
            "status": "failed" if failed else "passed",
            "checked": len(checks),
            "passed": passed,
            "failed": failed,
        },
        "checks": checks,
    }


def render_doctor(payload: dict[str, Any], format_name: str = "markdown") -> str:
    if format_name == "json":
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if format_name == "markdown":
        return _render_markdown(payload)
    raise ValueError(f"unsupported doctor format: {format_name}")


def _check_config(path: str | Path) -> dict[str, Any]:
    try:
        validate_config(load_config(path))
    except Exception as exc:
        return _failed("config", path, str(exc))
    return _passed("config", path, "valid config")


def _check_artifact(name: str, path: str | Path, validator: Validator) -> dict[str, Any]:
    try:
        validator(load_artifact(path))
    except Exception as exc:
        return _failed(name, path, str(exc))
    return _passed(name, path, f"valid {name}")


def _passed(name: str, path: str | Path | None, message: str) -> dict[str, Any]:
    return _check(name, "passed", path, message)


def _failed(name: str, path: str | Path | None, message: str) -> dict[str, Any]:
    return _check(name, "failed", path, message)


def _check(name: str, status: str, path: str | Path | None, message: str) -> dict[str, Any]:
    return {
        "name": name,
        "status": status,
        "path": str(path) if path is not None else None,
        "message": message,
    }


def _render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# HyrumGuard doctor",
        "",
        f"- Status: {summary['status']}",
        f"- Checks: {summary['checked']}",
        f"- Failed: {summary['failed']}",
        "",
        "| Check | Status | Path | Message |",
        "|---|---|---|---|",
    ]
    for check in payload["checks"]:
        lines.append(
            f"| {check['name']} | {check['status']} | {check.get('path') or '-'} | {check['message']} |"
        )
    return "\n".join(lines) + "\n"
