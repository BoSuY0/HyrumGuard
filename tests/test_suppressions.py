import json
from pathlib import Path

import pytest

from hyrumguard.analysis import analyze_risks
from hyrumguard.canary import plan_canary
from hyrumguard.config import parse_simple_yaml
from hyrumguard.diff import parse_unified_diff
from hyrumguard.miners import mine_repository
from hyrumguard.reporters import render_json, render_markdown, render_sarif
from hyrumguard.synthesis import synthesize_contracts
from hyrumguard.validation import ValidationError, validate_config, validate_risks


FIXTURES = Path(__file__).parent / "fixtures"


def _lockfile():
    atoms = mine_repository(
        FIXTURES / "downstreams" / "python_client",
        target_package="demo_lib",
        dependent="python-client",
    )
    return synthesize_contracts(atoms, confidence_threshold=0.5)


def _diff():
    return parse_unified_diff((FIXTURES / "sample.diff").read_text())


def test_simple_yaml_config_supports_multiline_suppressions():
    config = parse_simple_yaml(
        """
version: 1
suppressions:
  - id: accepted-error-text
    subject: missing token
    type: error_regex
    reason: Accepted legacy client assertion while replacement ships.
    expires: 2099-12-31
"""
    )

    assert config["suppressions"] == [
        {
            "id": "accepted-error-text",
            "subject": "missing token",
            "type": "error_regex",
            "reason": "Accepted legacy client assertion while replacement ships.",
            "expires": "2099-12-31",
        }
    ]


def test_config_validation_accepts_auditable_suppressions():
    validate_config(
        {
            "suppressions": [
                {
                    "id": "accepted-error-text",
                    "subject": "missing token",
                    "type": "error_regex",
                    "reason": "Accepted legacy client assertion while replacement ships.",
                    "expires": "2099-12-31",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    ("suppression", "expected"),
    [
        ({"id": "missing-reason", "subject": "status"}, "reason"),
        ({"id": "missing-target", "reason": "Too broad."}, "risk_id, subject, or type"),
        ({"id": "bad-date", "subject": "status", "reason": "Temporary.", "expires": "soon"}, "expires"),
    ],
)
def test_config_validation_rejects_malformed_suppressions(suppression, expected):
    with pytest.raises(ValidationError, match=expected):
        validate_config({"suppressions": [suppression]})


def test_analysis_marks_suppressed_risks_without_dropping_evidence():
    baseline = analyze_risks(_lockfile(), _diff())
    risks = analyze_risks(
        _lockfile(),
        _diff(),
        suppressions=[
            {
                "id": "accepted-error-text",
                "subject": "missing token",
                "type": "error_regex",
                "reason": "Accepted legacy client assertion while replacement ships.",
                "expires": "2099-12-31",
            }
        ],
    )

    suppressed = next(risk for risk in risks["risks"] if risk["subject"] == "missing token")

    assert suppressed["suppressed"] is True
    assert suppressed["suppression"]["id"] == "accepted-error-text"
    assert suppressed["suppression"]["reason"].startswith("Accepted legacy")
    assert suppressed["evidence"]
    assert risks["summary"]["total_risk_count"] == baseline["summary"]["risk_count"]
    assert risks["summary"]["risk_count"] == baseline["summary"]["risk_count"] - 1
    assert risks["summary"]["suppressed_count"] == 1
    validate_risks(risks)


def test_expired_suppression_is_reported_but_not_applied():
    risks = analyze_risks(
        _lockfile(),
        _diff(),
        suppressions=[
            {
                "id": "expired-error-text",
                "subject": "missing token",
                "reason": "Old exception.",
                "expires": "2000-01-01",
            }
        ],
    )

    target = next(risk for risk in risks["risks"] if risk["subject"] == "missing token")

    assert target["suppressed"] is False
    assert risks["summary"]["suppressed_count"] == 0
    assert risks["summary"]["expired_suppression_count"] == 1
    assert risks["summary"]["expired_suppressions"] == ["expired-error-text"]
    assert risks["summary"]["risk_count"] == risks["summary"]["total_risk_count"]


def test_reporters_render_suppression_metadata():
    risks = analyze_risks(
        _lockfile(),
        _diff(),
        suppressions=[
            {
                "id": "accepted-error-text",
                "subject": "missing token",
                "reason": "Accepted legacy client assertion while replacement ships.",
            }
        ],
    )

    as_json = json.loads(render_json(risks))
    as_markdown = render_markdown(risks)
    sarif = json.loads(render_sarif(risks))
    sarif_result = next(result for result in sarif["runs"][0]["results"] if "missing token" in result["message"]["text"])

    assert as_json["summary"]["suppressed_count"] == 1
    assert "Suppressed: 1" in as_markdown
    assert "accepted-error-text" in as_markdown
    assert sarif_result["suppressions"][0]["kind"] == "external"
    assert sarif_result["suppressions"][0]["justification"].startswith("Accepted legacy")


def test_canary_ignores_suppressed_risks():
    plan = plan_canary(
        {
            "risks": [
                {
                    "subject": "missing token",
                    "severity": "medium",
                    "dependents": ["python-client"],
                    "contracts": [],
                    "suppressed": True,
                }
            ],
            "summary": {"risk_count": 0, "suppressed_count": 1},
        },
        dependents=[{"name": "python-client", "path": "tests/fixtures/downstreams/python_client"}],
        affected_only=True,
        execute=False,
    )

    assert plan["selected"] == []
