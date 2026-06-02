import json

from hyrumguard.config import starter_config_text
from hyrumguard.doctor import build_doctor_payload, render_doctor


def test_doctor_payload_passes_for_valid_config(tmp_path):
    config = tmp_path / ".hyrumguard.yml"
    config.write_text(starter_config_text())

    payload = build_doctor_payload(config=config)

    assert payload["schema_version"] == 1
    assert payload["summary"]["status"] == "passed"
    assert payload["summary"]["failed"] == 0
    assert payload["checks"][0]["name"] == "package"
    assert any(check["name"] == "config" and check["status"] == "passed" for check in payload["checks"])


def test_doctor_payload_reports_missing_artifact_as_failed(tmp_path):
    payload = build_doctor_payload(config=tmp_path / "missing.yml")

    assert payload["summary"]["status"] == "failed"
    assert payload["summary"]["failed"] == 1
    failed = next(check for check in payload["checks"] if check["status"] == "failed")
    assert failed["name"] == "config"
    assert "not found" in failed["message"]


def test_doctor_renders_markdown_and_json(tmp_path):
    config = tmp_path / ".hyrumguard.yml"
    config.write_text(starter_config_text())
    payload = build_doctor_payload(config=config)

    markdown = render_doctor(payload, "markdown")
    as_json = json.loads(render_doctor(payload, "json"))

    assert "# HyrumGuard doctor" in markdown
    assert "| config | passed |" in markdown
    assert as_json["summary"]["status"] == "passed"
