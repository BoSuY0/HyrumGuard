from __future__ import annotations

from typing import Any

from hyrumguard.diff import DiffFacts


SEVERITY_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3}


def analyze_risks(lockfile: dict[str, Any], diff: DiffFacts | dict[str, Any]) -> dict[str, Any]:
    facts = diff if isinstance(diff, DiffFacts) else _facts_from_dict(diff)
    risks: list[dict[str, Any]] = []
    for contract in lockfile.get("contracts", []):
        match_reason = _match_reason(contract, facts)
        if not match_reason:
            continue
        severity = _severity(contract)
        risks.append(
            {
                "id": f"risk-{contract['id']}",
                "subject": contract["subject"],
                "type": contract["type"],
                "target_package": contract.get("target_package"),
                "severity": severity,
                "reason": match_reason,
                "dependents": contract.get("downstreams", []),
                "contracts": [contract],
                "evidence": contract.get("evidence", []),
                "locations": [{"path": path} for path in facts.files],
            }
        )

    risks.sort(key=lambda item: (-SEVERITY_ORDER[item["severity"]], item["subject"]))
    return {
        "schema_version": 1,
        "summary": {
            "risk_count": len(risks),
            "highest_severity": _highest_severity(risks),
            "changed_files": facts.files,
            "changed_subjects": sorted(facts.changed_subjects),
        },
        "risks": risks,
    }


def _facts_from_dict(payload: dict[str, Any]) -> DiffFacts:
    return DiffFacts(
        files=list(payload.get("files", [])),
        added_lines=list(payload.get("added_lines", [])),
        removed_lines=list(payload.get("removed_lines", [])),
        changed_subjects=set(payload.get("changed_subjects", [])),
    )


def _match_reason(contract: dict[str, Any], facts: DiffFacts) -> str | None:
    subject = contract.get("subject", "")
    subjects = facts.changed_subjects
    if subject in subjects:
        return f"changed subject `{subject}`"
    last_segment = _last_segment(subject)
    if last_segment and last_segment in subjects:
        return f"changed related symbol `{last_segment}`"
    if contract.get("type") == "private_symbol_use" and _private_path_overlap(subject, facts.files):
        return f"changed private path related to `{subject}`"
    if contract.get("type") == "json_shape_expectation" and subject in _removed_string_literals(facts):
        return f"changed JSON key `{subject}`"
    if contract.get("type") == "error_regex" and subject in _removed_string_literals(facts):
        return f"changed error text `{subject}`"
    return None


def _last_segment(subject: str) -> str:
    return subject.replace("/", ".").split(".")[-1]


def _private_path_overlap(subject: str, files: list[str]) -> bool:
    subject_parts = {part for part in subject.replace("/", ".").split(".") if part.startswith("_")}
    if not subject_parts:
        return False
    return any(any(part in path for part in subject_parts) for path in files)


def _removed_string_literals(facts: DiffFacts) -> set[str]:
    literals = set()
    for item in facts.removed_lines:
        for subject in facts.changed_subjects:
            if subject in item:
                literals.add(subject)
    return literals


def _severity(contract: dict[str, Any]) -> str:
    if contract.get("type") == "private_symbol_use":
        return "high"
    if contract.get("type") in {"error_regex", "json_shape_expectation"}:
        return "medium"
    return "low"


def _highest_severity(risks: list[dict[str, Any]]) -> str:
    if not risks:
        return "none"
    return max((risk["severity"] for risk in risks), key=lambda value: SEVERITY_ORDER[value])
