import json
import subprocess
import sys
import tarfile
from pathlib import Path

import hyrumguard
from hyrumguard.canary import plan_canary


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "hyrumguard.cli", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_release_metadata_files_exist_and_pyproject_has_quality_gates():
    pyproject = (ROOT / "pyproject.toml").read_text()

    assert (ROOT / "LICENSE").exists()
    assert (ROOT / "CHANGELOG.md").exists()
    assert (ROOT / "hyrumguard" / "py.typed").exists()
    assert hyrumguard.__version__ == "1.0.0"
    assert 'version = "1.0.0"' in pyproject
    assert "Homepage" in pyproject
    assert "build>=1" in pyproject
    assert "ruff>=0.8" in pyproject
    assert "mypy>=1" in pyproject
    assert "twine>=6" in pyproject
    assert 'package-data = {"hyrumguard" = ["py.typed"]}' in pyproject


def test_validate_accepts_good_lockfile_risks_and_sarif(tmp_path):
    dependents = tmp_path / "dependents.json"
    lockfile = tmp_path / "shadow-contracts.lock.json"
    risks = tmp_path / "risks.json"
    sarif = tmp_path / "hyrumguard.sarif"

    dependents.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "target": {"package": "demo_lib"},
                "dependents": [
                    {
                        "name": "python-client",
                        "path": str(ROOT / "tests" / "fixtures" / "downstreams" / "python_client"),
                        "target_package": "demo_lib",
                    }
                ],
            }
        )
    )

    infer = run_cli("infer", "--from", str(dependents), "--out", str(lockfile))
    assert infer.returncode == 0, infer.stderr
    check = run_cli(
        "check",
        "--contracts",
        str(lockfile),
        "--diff-file",
        str(ROOT / "tests" / "fixtures" / "sample.diff"),
        "--out",
        str(risks),
    )
    assert check.returncode == 0, check.stderr
    report = run_cli("report", "--risks", str(risks), "--format", "sarif", "--out", str(sarif))
    assert report.returncode == 0, report.stderr

    validate = run_cli(
        "validate",
        "--dependents",
        str(dependents),
        "--contracts",
        str(lockfile),
        "--risks",
        str(risks),
        "--sarif",
        str(sarif),
    )

    assert validate.returncode == 0, validate.stderr
    assert "validated 4 artifact(s)" in validate.stdout


def test_validate_rejects_malformed_lockfile_without_traceback(tmp_path):
    bad_lockfile = tmp_path / "bad-lockfile.json"
    bad_lockfile.write_text(json.dumps({"contracts": [{"id": "missing-required-fields"}]}))

    result = run_cli("validate", "--contracts", str(bad_lockfile))

    assert result.returncode == 2
    assert "invalid contracts" in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_invalid_input_uses_concise_error_without_traceback(tmp_path):
    missing = tmp_path / "missing.json"

    result = run_cli("infer", "--from", str(missing), "--out", str(tmp_path / "out.json"))

    assert result.returncode == 2
    assert "error:" in result.stderr
    assert "Traceback" not in result.stderr


def test_canary_execute_requires_unsafe_acknowledgement(tmp_path):
    risks = tmp_path / "risks.json"
    dependents = tmp_path / "dependents.json"

    risks.write_text(json.dumps({"schema_version": 1, "summary": {"risk_count": 0}, "risks": []}))
    dependents.write_text(json.dumps({"dependents": []}))

    result = run_cli("canary", "--risks", str(risks), "--dependents", str(dependents), "--execute")

    assert result.returncode == 2
    assert "--allow-unsafe-execution" in result.stderr
    assert "Traceback" not in result.stderr


def test_canary_execute_uses_temp_directory_and_reports_timeout(tmp_path):
    source = tmp_path / "dependent"
    source.mkdir()
    risks = {"risks": [{"subject": "missing token", "dependents": ["python-client"]}]}

    passed = plan_canary(
        risks,
        dependents=[
            {
                "name": "python-client",
                "path": str(source),
                "test_command": f"{sys.executable} -c \"from pathlib import Path; Path('created.txt').write_text('ok')\"",
            }
        ],
        affected_only=True,
        execute=True,
        timeout_seconds=5,
    )

    assert passed["results"][0]["status"] == "passed"
    assert not (source / "created.txt").exists()

    timed_out = plan_canary(
        risks,
        dependents=[
            {
                "name": "python-client",
                "path": str(source),
                "test_command": f"{sys.executable} -c \"import time; time.sleep(2)\"",
            }
        ],
        affected_only=True,
        execute=True,
        timeout_seconds=1,
    )

    assert timed_out["results"][0]["status"] == "timeout"


def test_source_distribution_contains_release_docs(tmp_path):
    dist = tmp_path / "dist"
    result = subprocess.run(
        [sys.executable, "-m", "build", "--sdist", "--outdir", str(dist)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    archive = next(dist.glob("hyrumguard-1.0.0.tar.gz"))
    with tarfile.open(archive) as tar:
        names = set(tar.getnames())

    assert "hyrumguard-1.0.0/LICENSE" in names
    assert "hyrumguard-1.0.0/CHANGELOG.md" in names
    assert "hyrumguard-1.0.0/hyrumguard/py.typed" in names
