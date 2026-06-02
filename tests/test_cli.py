import json
import subprocess
import sys
from pathlib import Path


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
    ]:
        result = run_cli(*args)
        assert result.returncode == 0, result.stderr
        assert "hyrumguard" in result.stdout.lower()


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
