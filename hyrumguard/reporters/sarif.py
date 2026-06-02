from __future__ import annotations

import json
from typing import Any


def render_sarif(risks: dict[str, Any]) -> str:
    results = []
    rules = {}
    for risk in risks.get("risks", []):
        rule_id = f"hyrumguard.{risk['type']}"
        rules[rule_id] = {
            "id": rule_id,
            "name": risk["type"],
            "shortDescription": {"text": f"HyrumGuard {risk['type']} risk"},
        }
        location = _location_for(risk)
        results.append(
            {
                "ruleId": rule_id,
                "level": _level(risk.get("severity", "low")),
                "message": {"text": f"{risk['subject']}: {risk['reason']}"},
                "locations": [location],
                "properties": {
                    "dependents": risk.get("dependents", []),
                    "target_package": risk.get("target_package"),
                },
            }
        )

    payload = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "HyrumGuard",
                        "informationUri": "https://github.com/hyrumguard/hyrumguard",
                        "rules": sorted(rules.values(), key=lambda item: item["id"]),
                    }
                },
                "results": results,
            }
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _location_for(risk: dict[str, Any]) -> dict[str, Any]:
    locations = risk.get("locations") or [{"path": "unknown"}]
    path = locations[0].get("path") or "unknown"
    return {"physicalLocation": {"artifactLocation": {"uri": path}, "region": {"startLine": 1}}}


def _level(severity: str) -> str:
    return {"high": "error", "medium": "warning", "low": "note"}.get(severity, "note")
