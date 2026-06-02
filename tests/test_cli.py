import json
import subprocess
import sys
from pathlib import Path

from hyrumguard.config import load_config
from hyrumguard.validation import validate_config


FIXTURES = Path(__file__).parent / "fixtures"


def run_cli(*args, cwd=None):
    return subprocess.run(
        [sys.executable, "-m", "hyrumguard.cli", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_help_commands_exit_zero():
    for args in [
        (),
        ("discover", "--help"),
        ("infer", "--help"),
        ("check", "--help"),
        ("canary", "--help"),
        ("report", "--help"),
        ("validate", "--help"),
        ("init", "--help"),
        ("explain", "--help"),
    ]:
        result = run_cli(*args)
        assert result.returncode == 0, result.stderr
        assert "hyrumguard" in result.stdout.lower()


def test_cli_init_writes_default_config(tmp_path):
    result = run_cli("init", cwd=tmp_path)
    config = tmp_path / ".hyrumguard.yml"

    assert result.returncode == 0, result.stderr
    assert config.exists()
    text = config.read_text()
    assert "target:" in text
    assert "suppressions:" in text
    validate_config(load_config(config))
    assert "wrote starter config" in result.stdout


def test_cli_init_supports_custom_path(tmp_path):
    result = run_cli("init", "--path", "config/hyrumguard.yml", cwd=tmp_path)
    config = tmp_path / "config" / "hyrumguard.yml"

    assert result.returncode == 0, result.stderr
    assert config.exists()
    assert "config/hyrumguard.yml" in result.stdout


def test_cli_init_refuses_to_overwrite_without_flag(tmp_path):
    config = tmp_path / ".hyrumguard.yml"
    config.write_text("existing: true\n")

    result = run_cli("init", cwd=tmp_path)

    assert result.returncode == 2
    assert "--overwrite" in result.stderr
    assert "Traceback" not in result.stderr
    assert config.read_text() == "existing: true\n"


def test_cli_init_overwrites_with_explicit_flag(tmp_path):
    config = tmp_path / ".hyrumguard.yml"
    config.write_text("existing: true\n")

    result = run_cli("init", "--overwrite", cwd=tmp_path)

    assert result.returncode == 0, result.stderr
    assert "existing: true" not in config.read_text()
    assert "version: 1" in config.read_text()


def test_cli_infer_check_report_flow(tmp_path):
    dependents = tmp_path / "dependents.json"
    lockfile = tmp_path / "shadow-contracts.lock.json"
    risks = tmp_path / "risks.json"
    markdown = tmp_path / "report.md"
    sarif = tmp_path / "hyrumguard.sarif"

    dependents.write_text(
        json.dumps(
            {
                "dependents": [
                    {
                        "name": "python-client",
                        "path": str(FIXTURES / "downstreams" / "python_client"),
                        "target_package": "demo_lib",
                    }
                ]
            }
        )
    )

    infer = run_cli("infer", "--from", str(dependents), "--out", str(lockfile))
    assert infer.returncode == 0, infer.stderr
    assert lockfile.exists()

    check = run_cli(
        "check",
        "--contracts",
        str(lockfile),
        "--diff-file",
        str(FIXTURES / "sample.diff"),
        "--out",
        str(risks),
    )
    assert check.returncode == 0, check.stderr
    assert json.loads(risks.read_text())["summary"]["risk_count"] >= 3

    report_md = run_cli("report", "--risks", str(risks), "--format", "markdown", "--out", str(markdown))
    assert report_md.returncode == 0, report_md.stderr
    assert "implicit compatibility" in markdown.read_text()

    report_sarif = run_cli("report", "--risks", str(risks), "--format", "sarif", "--out", str(sarif))
    assert report_sarif.returncode == 0, report_sarif.stderr
    assert json.loads(sarif.read_text())["version"] == "2.1.0"


def test_cli_check_applies_configured_suppressions(tmp_path):
    dependents = tmp_path / "dependents.json"
    lockfile = tmp_path / "shadow-contracts.lock.json"
    risks = tmp_path / "risks.json"
    config = tmp_path / ".hyrumguard.yml"

    dependents.write_text(
        json.dumps(
            {
                "dependents": [
                    {
                        "name": "python-client",
                        "path": str(FIXTURES / "downstreams" / "python_client"),
                        "target_package": "demo_lib",
                    }
                ]
            }
        )
    )
    config.write_text(
        """
version: 1
suppressions:
  - id: accepted-error-text
    subject: missing token
    type: error_regex
    reason: Accepted legacy client assertion while replacement ships.
"""
    )

    infer = run_cli("infer", "--from", str(dependents), "--out", str(lockfile))
    assert infer.returncode == 0, infer.stderr

    check = run_cli(
        "check",
        "--contracts",
        str(lockfile),
        "--diff-file",
        str(FIXTURES / "sample.diff"),
        "--config",
        str(config),
        "--out",
        str(risks),
    )

    payload = json.loads(risks.read_text())
    suppressed = next(risk for risk in payload["risks"] if risk["subject"] == "missing token")

    assert check.returncode == 0, check.stderr
    assert payload["summary"]["suppressed_count"] == 1
    assert payload["summary"]["risk_count"] == payload["summary"]["total_risk_count"] - 1
    assert suppressed["suppressed"] is True
    assert suppressed["suppression"]["id"] == "accepted-error-text"


def test_cli_explain_writes_markdown_and_json(tmp_path):
    risks = tmp_path / "risks.json"
    markdown = tmp_path / "explanation.md"
    as_json = tmp_path / "explanation.json"
    payload = {
        "schema_version": 1,
        "summary": {"risk_count": 0, "total_risk_count": 1, "suppressed_count": 1},
        "risks": [
            {
                "id": "risk-contract-1",
                "subject": "missing token",
                "type": "error_regex",
                "severity": "medium",
                "reason": "changed error text `missing token`",
                "dependents": ["python-client"],
                "contracts": [
                    {
                        "id": "contract-1",
                        "type": "error_regex",
                        "subject": "missing token",
                        "confidence": 0.8,
                    }
                ],
                "evidence": [
                    {
                        "dependent": "python-client",
                        "path": "tests/test_usage.py",
                        "line": 12,
                        "snippet": "assert 'missing token' in message",
                    }
                ],
                "locations": [{"path": "src/errors.py"}],
                "suppressed": True,
                "suppression": {
                    "id": "accepted-error-text",
                    "reason": "Accepted legacy client assertion while replacement ships.",
                    "matched_on": ["subject", "type"],
                },
            }
        ],
    }
    risks.write_text(json.dumps(payload))

    markdown_result = run_cli(
        "explain",
        "--risks",
        str(risks),
        "--subject",
        "missing token",
        "--out",
        str(markdown),
    )
    json_result = run_cli(
        "explain",
        "--risks",
        str(risks),
        "--id",
        "risk-contract-1",
        "--format",
        "json",
        "--out",
        str(as_json),
    )

    assert markdown_result.returncode == 0, markdown_result.stderr
    assert "wrote markdown explanation" in markdown_result.stdout
    assert "Suppression: accepted-error-text" in markdown.read_text()
    assert json_result.returncode == 0, json_result.stderr
    assert json.loads(as_json.read_text())["summary"]["match_count"] == 1


def test_cli_explain_missing_match_uses_concise_error(tmp_path):
    risks = tmp_path / "risks.json"
    risks.write_text(json.dumps({"schema_version": 1, "summary": {"risk_count": 0}, "risks": []}))

    result = run_cli("explain", "--risks", str(risks), "--subject", "missing token")

    assert result.returncode == 2
    assert "no risks matched" in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_canary_dry_run(tmp_path):
    risks = tmp_path / "risks.json"
    dependents = tmp_path / "dependents.json"
    output = tmp_path / "canary.json"

    risks.write_text(
        json.dumps(
            {
                "risks": [
                    {
                        "subject": "missing token",
                        "severity": "medium",
                        "dependents": ["python-client"],
                        "contracts": [],
                    }
                ],
                "summary": {"risk_count": 1},
            }
        )
    )
    dependents.write_text(
        json.dumps(
            {
                "dependents": [
                    {"name": "python-client", "path": "tests/fixtures/downstreams/python_client", "test_command": "pytest -q"},
                    {"name": "other-client", "path": "tests/fixtures/downstreams/other", "test_command": "pytest -q"},
                ]
            }
        )
    )

    result = run_cli(
        "canary",
        "--risks",
        str(risks),
        "--dependents",
        str(dependents),
        "--affected-only",
        "--out",
        str(output),
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(output.read_text())["selected"][0]["name"] == "python-client"
