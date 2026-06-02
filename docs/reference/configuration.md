# Configuration

HyrumGuard reads a small YAML or JSON config. The bundled parser supports the simple YAML subset used here.

```yaml
version: 1

target:
  ecosystem: pypi
  package: demo_lib

discovery:
  top_dependents: 40
  ecosystems:
    - manual
    - pypi
  seeds:
    - python-client=tests/fixtures/downstreams/python_client

contracts:
  infer:
    - symbol_use
    - private_symbol_use
    - error_regex
    - json_shape_expectation
  confidence_threshold: 0.72

canary:
  enabled: true
  affected_only: true
  max_repositories: 8
  timeout_seconds: 300

reporting:
  markdown: true
  sarif: true
  json_artifact: true
```

## Manual Seeds

Manual seeds use `name=path`:

```yaml
discovery:
  seeds:
    - python-client=tests/fixtures/downstreams/python_client
```

The CLI also accepts manual seeds:

```bash
hyrumguard discover demo_lib --seed python-client=tests/fixtures/downstreams/python_client
```

## Runtime Artifacts

Runtime artifacts are written under `.hyrum/` by default and are ignored by this repository's `.gitignore`. A maintainer can choose to commit `shadow-contracts.lock.json` in their own project when they want a stable shadow-contract baseline.

## Validation

Validate config and generated artifacts before using them in CI decisions:

```bash
hyrumguard validate \
  --config .hyrumguard.yml \
  --dependents .hyrum/dependents.json \
  --contracts .hyrum/shadow-contracts.lock.json \
  --risks .hyrum/risks.json \
  --sarif hyrumguard.sarif
```
