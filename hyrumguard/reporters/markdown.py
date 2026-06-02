from __future__ import annotations

from typing import Any


def render_markdown(risks: dict[str, Any]) -> str:
    summary = risks.get("summary", {})
    lines = [
        "# HyrumGuard implicit compatibility report",
        "",
        f"- Risks: {summary.get('risk_count', 0)}",
        f"- Highest severity: {summary.get('highest_severity', 'none')}",
        "",
    ]
    if not risks.get("risks"):
        lines.append("No shadow-contract risks were matched against this diff.")
        return "\n".join(lines) + "\n"

    lines.extend(["| Severity | Type | Subject | Dependents | Reason |", "|---|---|---|---|---|"])
    for risk in risks["risks"]:
        dependents = ", ".join(risk.get("dependents", [])) or "-"
        lines.append(
            f"| {risk['severity']} | {risk['type']} | `{risk['subject']}` | {dependents} | {risk['reason']} |"
        )
    lines.append("")
    lines.append("## Evidence")
    for risk in risks["risks"]:
        lines.append(f"- `{risk['subject']}`")
        for evidence in risk.get("evidence", [])[:3]:
            lines.append(
                f"  - {evidence.get('dependent')} `{evidence.get('path')}:{evidence.get('line')}`: "
                f"{evidence.get('snippet')}"
            )
    return "\n".join(lines) + "\n"
