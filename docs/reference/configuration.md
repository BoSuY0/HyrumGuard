# Configuration

HyrumGuard reads a small YAML or JSON config. The bundled parser supports the simple YAML subset used here.

Create a starter config:

```bash
hyrumguard init
```

Use `--path` for a custom location and `--overwrite` only when replacing an existing config intentionally:

```bash
hyrumguard init --path config/hyrumguard.yml
hyrumguard init --overwrite
```

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

suppressions: []
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

## Suppressions

Suppression entries let maintainers accept known risks without deleting the audit trail. A suppression requires:

- `id`: stable local identifier for review and SARIF metadata
- `reason`: why the finding is accepted
- at least one target matcher: `risk_id`, `subject`, or `type`

Optional `expires` must be an ISO date such as `2026-12-31`. Expired suppressions are reported in `summary.expired_suppression_count` and do not suppress matching risks.

When suppressions apply, the risk remains in `.hyrum/risks.json` with `suppressed: true` and a `suppression` object. `summary.risk_count` counts active unsuppressed risks, while `summary.total_risk_count` and `summary.suppressed_count` preserve the full audit count.

Run `check` with config to apply suppressions:

```bash
hyrumguard check \
  --contracts .hyrum/shadow-contracts.lock.json \
  --base origin/main \
  --head HEAD \
  --config .hyrumguard.yml
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
