from __future__ import annotations

import json
from typing import Any


class ExplanationError(ValueError):
    """Raised when a targeted risk explanation cannot be rendered."""


def explain_risks(
    risks_payload: dict[str, Any],
    risk_id: str | None = None,
    subject: str | None = None,
    format_name: str = "markdown",
) -> str:
    matches = _select_risks(risks_payload, risk_id=risk_id, subject=subject)
    payload = {
        "schema_version": 1,
        "summary": {
            "match_count": len(matches),
            "selector": {"id": risk_id, "subject": subject},
        },
        "explanations": [_explanation_for(risk) for risk in matches],
    }
    if format_name == "json":
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if format_name == "markdown":
        return _render_markdown(payload)
    raise ExplanationError(f"unsupported explanation format: {format_name}")


def _select_risks(
    risks_payload: dict[str, Any],
    risk_id: str | None,
    subject: str | None,
) -> list[dict[str, Any]]:
    if not risk_id and not subject:
        raise ExplanationError("pass --id or --subject to select a risk")
    risks = risks_payload.get("risks", [])
    matches = [
        risk
        for risk in risks
        if (not risk_id or risk.get("id") == risk_id) and (not subject or risk.get("subject") == subject)
    ]
    if not matches:
        selector = risk_id or subject or "unknown"
        raise ExplanationError(f"no risks matched {selector!r}")
    return matches


def _explanation_for(risk: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": risk.get("id"),
        "subject": risk.get("subject"),
        "type": risk.get("type"),
        "severity": risk.get("severity"),
        "reason": risk.get("reason"),
        "dependents": risk.get("dependents", []),
        "locations": risk.get("locations", []),
        "suppressed": bool(risk.get("suppressed")),
        "suppression": risk.get("suppression"),
        "evidence": risk.get("evidence", []),
        "contracts": risk.get("contracts", []),
    }


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# HyrumGuard risk explanation",
        "",
        f"- Matches: {payload['summary']['match_count']}",
        "",
    ]
    for explanation in payload["explanations"]:
        lines.extend(_render_explanation(explanation))
    return "\n".join(lines) + "\n"


def _render_explanation(explanation: dict[str, Any]) -> list[str]:
    lines = [
        f"## `{explanation['subject']}`",
        "",
        f"- ID: `{explanation['id']}`",
        f"- Type: `{explanation['type']}`",
        f"- Severity: {explanation['severity']}",
        f"- Status: {'suppressed' if explanation['suppressed'] else 'active'}",
        f"- Reason: {explanation['reason']}",
        f"- Dependents: {_join_or_dash(explanation['dependents'])}",
    ]
    if explanation.get("suppressed"):
        suppression = explanation.get("suppression") or {}
        lines.append(f"- Suppression: {suppression.get('id', 'unknown')} - {suppression.get('reason', '')}")
    locations = [item.get("path", "unknown") for item in explanation.get("locations", [])]
    lines.append(f"- Changed locations: {_join_or_dash(locations)}")
    lines.extend(["", "### Evidence"])
    evidence = explanation.get("evidence", [])
    if not evidence:
        lines.append("- No evidence snippets recorded.")
    for item in evidence[:5]:
        lines.append(
            f"- {item.get('dependent', 'unknown')} `{item.get('path', 'unknown')}:{item.get('line', '?')}`: "
            f"{item.get('snippet', '')}"
        )
    lines.extend(["", "### Contracts"])
    contracts = explanation.get("contracts", [])
    if not contracts:
        lines.append("- No contract payloads recorded.")
    for contract in contracts[:5]:
        lines.append(
            f"- `{contract.get('id', 'unknown')}` {contract.get('type', 'unknown')} "
            f"`{contract.get('subject', 'unknown')}` confidence={contract.get('confidence', 'unknown')}"
        )
    lines.append("")
    return lines


def _join_or_dash(values: list[Any]) -> str:
    rendered = [str(value) for value in values if value]
    return ", ".join(rendered) if rendered else "-"
