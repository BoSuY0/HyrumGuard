from __future__ import annotations

from copy import deepcopy
from datetime import date
from typing import Any


SEVERITY_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3}
MATCH_FIELDS = ("risk_id", "subject", "type")


def apply_suppressions(
    risks_payload: dict[str, Any],
    suppressions: list[dict[str, Any]] | None,
    today: date | None = None,
) -> dict[str, Any]:
    payload = deepcopy(risks_payload)
    current_date = today or date.today()
    active, expired = _partition_suppressions(suppressions or [], current_date)

    suppressed_count = 0
    for risk in payload.get("risks", []):
        suppression = _matching_suppression(risk, active)
        if suppression:
            risk["suppressed"] = True
            risk["suppression"] = suppression
            suppressed_count += 1
        else:
            risk["suppressed"] = False

    risks = payload.get("risks", [])
    active_risks = [risk for risk in risks if not risk.get("suppressed")]
    summary = payload.setdefault("summary", {})
    summary["risk_count"] = len(active_risks)
    summary["total_risk_count"] = len(risks)
    summary["suppressed_count"] = suppressed_count
    summary["expired_suppression_count"] = len(expired)
    summary["highest_severity"] = _highest_severity(active_risks)
    if expired:
        summary["expired_suppressions"] = [item["id"] for item in expired]
    else:
        summary.pop("expired_suppressions", None)
    return payload


def _partition_suppressions(
    suppressions: list[dict[str, Any]],
    current_date: date,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    active: list[dict[str, Any]] = []
    expired: list[dict[str, Any]] = []
    for raw in suppressions:
        suppression = _public_suppression(raw)
        if _is_expired(suppression, current_date):
            expired.append(suppression)
        else:
            active.append(suppression)
    return active, expired


def _public_suppression(raw: dict[str, Any]) -> dict[str, Any]:
    suppression = {
        "id": str(raw.get("id", "")),
        "reason": str(raw.get("reason", "")),
    }
    for field in MATCH_FIELDS:
        if raw.get(field) is not None:
            suppression[field] = str(raw[field])
    if raw.get("expires") is not None:
        suppression["expires"] = str(raw["expires"])
    return suppression


def _is_expired(suppression: dict[str, Any], current_date: date) -> bool:
    expires = suppression.get("expires")
    if not expires:
        return False
    try:
        return date.fromisoformat(str(expires)) < current_date
    except ValueError:
        return False


def _matching_suppression(risk: dict[str, Any], suppressions: list[dict[str, Any]]) -> dict[str, Any] | None:
    for suppression in suppressions:
        matched_on = _matched_fields(risk, suppression)
        if matched_on:
            return {**suppression, "matched_on": matched_on}
    return None


def _matched_fields(risk: dict[str, Any], suppression: dict[str, Any]) -> list[str]:
    fields = [field for field in MATCH_FIELDS if field in suppression]
    if not fields:
        return []
    for field in fields:
        risk_value = risk["id"] if field == "risk_id" else risk.get(field)
        if str(risk_value) != suppression[field]:
            return []
    return fields


def _highest_severity(risks: list[dict[str, Any]]) -> str:
    if not risks:
        return "none"
    return max((risk["severity"] for risk in risks), key=lambda value: SEVERITY_ORDER[value])
