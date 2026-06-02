from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


class ValidationError(ValueError):
    """Raised when a HyrumGuard artifact is malformed."""


def load_artifact(path: str | Path) -> Any:
    artifact_path = Path(path)
    try:
        return json.loads(artifact_path.read_text())
    except FileNotFoundError as exc:
        raise ValidationError(f"file not found: {artifact_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {artifact_path}: {exc.msg}") from exc


def validate_config(config: dict[str, Any]) -> None:
    if not isinstance(config, dict):
        raise ValidationError("invalid config: root must be an object")
    if "target" in config:
        target = _require_object(config, "target", "config")
        _optional_string(target, "package", "config.target")
        _optional_string(target, "ecosystem", "config.target")
    if "discovery" in config:
        discovery = _require_object(config, "discovery", "config")
        if "seeds" in discovery and not isinstance(discovery["seeds"], list):
            raise ValidationError("invalid config.discovery.seeds: must be a list")
        if "ecosystems" in discovery and not isinstance(discovery["ecosystems"], list | str):
            raise ValidationError("invalid config.discovery.ecosystems: must be a list or string")
    if "suppressions" in config:
        suppressions = config["suppressions"]
        if not isinstance(suppressions, list):
            raise ValidationError("invalid config.suppressions: must be a list")
        for index, suppression in enumerate(suppressions):
            _validate_suppression(suppression, f"config.suppressions[{index}]")


def validate_dependents(payload: dict[str, Any]) -> None:
    if not isinstance(payload, dict):
        raise ValidationError("invalid dependents: root must be an object")
    dependents = payload.get("dependents")
    if not isinstance(dependents, list):
        raise ValidationError("invalid dependents: `dependents` must be a list")
    for index, dependent in enumerate(dependents):
        if not isinstance(dependent, dict):
            raise ValidationError(f"invalid dependents[{index}]: must be an object")
        _require_string(dependent, "name", f"dependents[{index}]")
        if "path" in dependent:
            _require_string(dependent, "path", f"dependents[{index}]")


def validate_lockfile(payload: dict[str, Any]) -> None:
    if not isinstance(payload, dict):
        raise ValidationError("invalid contracts: root must be an object")
    if payload.get("schema_version") != 1:
        raise ValidationError("invalid contracts: schema_version must be 1")
    contracts = payload.get("contracts")
    if not isinstance(contracts, list):
        raise ValidationError("invalid contracts: `contracts` must be a list")
    required = {"id", "type", "target_package", "subject", "confidence", "downstreams", "atoms", "evidence"}
    for index, contract in enumerate(contracts):
        if not isinstance(contract, dict):
            raise ValidationError(f"invalid contracts[{index}]: must be an object")
        missing = sorted(required - set(contract))
        if missing:
            raise ValidationError(f"invalid contracts[{index}]: missing {', '.join(missing)}")
        if not isinstance(contract["downstreams"], list):
            raise ValidationError(f"invalid contracts[{index}].downstreams: must be a list")
        if not isinstance(contract["atoms"], list):
            raise ValidationError(f"invalid contracts[{index}].atoms: must be a list")


def validate_risks(payload: dict[str, Any]) -> None:
    if not isinstance(payload, dict):
        raise ValidationError("invalid risks: root must be an object")
    if payload.get("schema_version") != 1:
        raise ValidationError("invalid risks: schema_version must be 1")
    summary = _require_object(payload, "summary", "risks")
    if "risk_count" not in summary:
        raise ValidationError("invalid risks.summary: missing risk_count")
    risks = payload.get("risks")
    if not isinstance(risks, list):
        raise ValidationError("invalid risks: `risks` must be a list")
    required = {"id", "subject", "type", "severity", "reason", "dependents", "contracts"}
    for index, risk in enumerate(risks):
        if not isinstance(risk, dict):
            raise ValidationError(f"invalid risks[{index}]: must be an object")
        missing = sorted(required - set(risk))
        if missing:
            raise ValidationError(f"invalid risks[{index}]: missing {', '.join(missing)}")
        if "suppressed" in risk and not isinstance(risk["suppressed"], bool):
            raise ValidationError(f"invalid risks[{index}].suppressed: must be a boolean")
        if risk.get("suppressed"):
            suppression = _require_object(risk, "suppression", f"risks[{index}]")
            _require_string(suppression, "id", f"risks[{index}].suppression")
            _require_string(suppression, "reason", f"risks[{index}].suppression")


def validate_sarif(payload: dict[str, Any]) -> None:
    if not isinstance(payload, dict):
        raise ValidationError("invalid SARIF: root must be an object")
    if payload.get("version") != "2.1.0":
        raise ValidationError("invalid SARIF: version must be 2.1.0")
    runs = payload.get("runs")
    if not isinstance(runs, list) or not runs:
        raise ValidationError("invalid SARIF: runs must be a non-empty list")
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            raise ValidationError(f"invalid SARIF runs[{index}]: must be an object")
        tool = _require_object(run, "tool", f"SARIF runs[{index}]")
        driver = _require_object(tool, "driver", f"SARIF runs[{index}].tool")
        if driver.get("name") != "HyrumGuard":
            raise ValidationError(f"invalid SARIF runs[{index}].tool.driver.name: expected HyrumGuard")


def _require_object(payload: dict[str, Any], key: str, label: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ValidationError(f"invalid {label}.{key}: must be an object")
    return value


def _require_string(payload: dict[str, Any], key: str, label: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationError(f"invalid {label}.{key}: must be a non-empty string")
    return value


def _optional_string(payload: dict[str, Any], key: str, label: str) -> None:
    if key in payload and not isinstance(payload[key], str):
        raise ValidationError(f"invalid {label}.{key}: must be a string")


def _validate_suppression(value: Any, label: str) -> None:
    if not isinstance(value, dict):
        raise ValidationError(f"invalid {label}: must be an object")
    _require_string(value, "id", label)
    _require_string(value, "reason", label)
    for key in ("risk_id", "subject", "type", "expires"):
        _optional_string(value, key, label)
    if not any(value.get(key) for key in ("risk_id", "subject", "type")):
        raise ValidationError(f"invalid {label}: must set at least one of risk_id, subject, or type")
    if value.get("expires"):
        try:
            date.fromisoformat(value["expires"])
        except ValueError as exc:
            raise ValidationError(f"invalid {label}.expires: must be an ISO date like 2026-12-31") from exc
