import json
from pathlib import Path

from hyrumguard.analysis import analyze_risks
from hyrumguard.canary import plan_canary
from hyrumguard.diff import parse_unified_diff
from hyrumguard.miners import mine_repository
from hyrumguard.reporters import render_json, render_markdown, render_sarif
from hyrumguard.synthesis import synthesize_contracts


FIXTURES = Path(__file__).parent / "fixtures"


def _lockfile():
    atoms = mine_repository(
        FIXTURES / "downstreams" / "python_client",
        target_package="demo_lib",
        dependent="python-client",
    )
    return synthesize_contracts(atoms, confidence_threshold=0.5)


def test_check_maps_diff_to_shadow_contract_risks():
    diff = parse_unified_diff((FIXTURES / "sample.diff").read_text())
    risks = analyze_risks(_lockfile(), diff)

    risk_subjects = {risk["subject"] for risk in risks["risks"]}

    assert "missing token" in risk_subjects
    assert "status" in risk_subjects
    assert "demo_lib._compat.normalize_payload" in risk_subjects
    assert risks["summary"]["risk_count"] >= 3
    assert risks["summary"]["highest_severity"] in {"medium", "high"}


def test_reporters_render_json_markdown_and_sarif():
    diff = parse_unified_diff((FIXTURES / "sample.diff").read_text())
    risks = analyze_risks(_lockfile(), diff)

    as_json = render_json(risks)
    as_markdown = render_markdown(risks)
    as_sarif = render_sarif(risks)

    assert json.loads(as_json)["summary"]["risk_count"] >= 3
    assert "HyrumGuard implicit compatibility report" in as_markdown
    assert "missing token" in as_markdown
    sarif = json.loads(as_sarif)
    assert sarif["version"] == "2.1.0"
    assert sarif["runs"][0]["tool"]["driver"]["name"] == "HyrumGuard"
    assert sarif["runs"][0]["results"]


def test_canary_defaults_to_changed_only_dry_run():
    diff = parse_unified_diff((FIXTURES / "sample.diff").read_text())
    risks = analyze_risks(_lockfile(), diff)

    plan = plan_canary(
        risks,
        dependents=[
            {"name": "python-client", "path": "tests/fixtures/downstreams/python_client", "test_command": "pytest -q"},
            {"name": "unaffected-client", "path": "tests/fixtures/downstreams/other", "test_command": "pytest -q"},
        ],
        affected_only=True,
        max_repos=8,
        execute=False,
    )

    assert plan["mode"] == "dry-run"
    assert [item["name"] for item in plan["selected"]] == ["python-client"]
    assert plan["selected"][0]["reason"].startswith("affected by")
