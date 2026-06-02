from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def plan_canary(
    risks: dict[str, Any],
    dependents: list[dict[str, Any]],
    affected_only: bool = True,
    max_repos: int = 8,
    execute: bool = False,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    affected = _affected_dependents(risks)
    selected: list[dict[str, Any]] = []
    for dependent in dependents:
        name = dependent.get("name") or dependent.get("repository") or dependent.get("path")
        if affected_only and name not in affected:
            continue
        item = dict(dependent)
        item["name"] = name
        item["reason"] = f"affected by {', '.join(sorted(affected.get(name, [])))}" if name in affected else "selected by configuration"
        selected.append(item)
        if len(selected) >= max_repos:
            break

    plan = {
        "schema_version": 1,
        "mode": "execute" if execute else "dry-run",
        "affected_only": affected_only,
        "max_repos": max_repos,
        "selected": selected,
        "results": [],
    }
    if execute:
        plan["results"] = [_execute_dependent(item, timeout_seconds) for item in selected]
    return plan


def _affected_dependents(risks: dict[str, Any]) -> dict[str, set[str]]:
    affected: dict[str, set[str]] = {}
    for risk in risks.get("risks", []):
        for dependent in risk.get("dependents", []):
            affected.setdefault(dependent, set()).add(risk.get("subject", "unknown"))
    return affected


def _execute_dependent(dependent: dict[str, Any], timeout_seconds: int) -> dict[str, Any]:
    command = dependent.get("test_command")
    source = dependent.get("path")
    if not command:
        return {"name": dependent["name"], "status": "skipped", "reason": "no test_command configured"}
    if not source or not Path(source).exists():
        return {"name": dependent["name"], "status": "failed", "reason": f"path not found: {source}"}

    with tempfile.TemporaryDirectory(prefix="hyrumguard-canary-") as temp_dir:
        workdir = Path(temp_dir) / "repo"
        shutil.copytree(source, workdir)
        try:
            result = subprocess.run(
                command,
                cwd=workdir,
                shell=True,
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return {
                "name": dependent["name"],
                "status": "timeout",
                "timeout_seconds": timeout_seconds,
                "stdout": _decode_tail(exc.stdout),
                "stderr": _decode_tail(exc.stderr),
            }
        return {
            "name": dependent["name"],
            "status": "passed" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "stdout": result.stdout[-4000:],
            "stderr": result.stderr[-4000:],
        }


def _decode_tail(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")[-4000:]
    return value[-4000:]
