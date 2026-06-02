from hyrumguard.config import parse_simple_yaml
from hyrumguard.discovery import discover_dependents, parse_seed


def test_simple_yaml_config_supports_examples():
    config = parse_simple_yaml(
        """
version: 1
target:
  ecosystem: pypi
  package: demo_lib
discovery:
  top_dependents: 2
  ecosystems:
    - manual
  seeds:
    - python-client=tests/fixtures/downstreams/python_client
contracts:
  confidence_threshold: 0.72
canary:
  enabled: true
"""
    )

    assert config["target"]["package"] == "demo_lib"
    assert config["discovery"]["ecosystems"] == ["manual"]
    assert config["discovery"]["seeds"][0].startswith("python-client=")
    assert config["canary"]["enabled"] is True


def test_discovery_accepts_manual_seeds_and_fake_ecosystems_client():
    payload = discover_dependents(
        "demo_lib",
        ecosystems=["manual", "pypi"],
        top=3,
        seeds=[parse_seed("python-client=tests/fixtures/downstreams/python_client")],
        fetcher=lambda _url: [
            {"name": "ecosystems-client", "repository_url": "https://example.test/repo", "stars": 10}
        ],
    )

    names = [item["name"] for item in payload["dependents"]]

    assert names == ["ecosystems-client", "python-client"]
    assert payload["target"]["package"] == "demo_lib"
