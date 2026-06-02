import json
from pathlib import Path

import pytest

from hyrumguard.analysis import analyze_risks
from hyrumguard.diff import parse_unified_diff
from hyrumguard.explain import ExplanationError, explain_risks
from hyrumguard.miners import mine_repository
from hyrumguard.synthesis import synthesize_contracts


FIXTURES = Path(__file__).parent / "fixtures"


def _risk_payload():
    atoms = mine_repository(
        FIXTURES / "downstreams" / "python_client",
        target_package="demo_lib",
        dependent="python-client",
    )
    lockfile = synthesize_contracts(atoms, confidence_threshold=0.5)
    diff = parse_unified_diff((FIXTURES / "sample.diff").read_text())
    return analyze_risks(
        lockfile,
        diff,
        suppressions=[
            {
                "id": "accepted-error-text",
                "subject": "missing token",
                "type": "error_regex",
                "reason": "Accepted legacy client assertion while replacement ships.",
            }
        ],
    )


def test_explain_renders_markdown_for_subject_match():
    rendered = explain_risks(_risk_payload(), subject="missing token", format_name="markdown")

    assert "# HyrumGuard risk explanation" in rendered
    assert "`missing token`" in rendered
    assert "Suppression: accepted-error-text" in rendered
    assert "Accepted legacy client assertion" in rendered
    assert "python-client" in rendered
    assert "Evidence" in rendered


def test_explain_renders_json_for_risk_id_match():
    risks = _risk_payload()
    risk_id = next(risk["id"] for risk in risks["risks"] if risk["subject"] == "missing token")

    rendered = explain_risks(risks, risk_id=risk_id, format_name="json")
    payload = json.loads(rendered)

    assert payload["schema_version"] == 1
    assert payload["summary"]["match_count"] == 1
    explanation = payload["explanations"][0]
    assert explanation["id"] == risk_id
    assert explanation["suppressed"] is True
    assert explanation["suppression"]["id"] == "accepted-error-text"
    assert explanation["evidence"]
    assert explanation["contracts"]


def test_explain_requires_a_selector():
    with pytest.raises(ExplanationError, match="pass --id or --subject"):
        explain_risks(_risk_payload(), format_name="markdown")


def test_explain_reports_missing_match():
    with pytest.raises(ExplanationError, match="no risks matched"):
        explain_risks(_risk_payload(), subject="does-not-exist", format_name="markdown")
