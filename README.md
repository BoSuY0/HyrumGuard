# HyrumGuard

HyrumGuard is an OSS maintainer tool for Hyrum's Law: it mines public downstream code and tests, turns implicit behavior dependencies into shadow contracts, and reports which contracts a PR may break before maintainers merge or publish.

Public release repository: [BoSuY0/HyrumGuard](https://github.com/BoSuY0/HyrumGuard).

The stable local release scope is intentionally narrow:

- npm/PyPI-oriented workflows.
- Python and JavaScript/TypeScript downstream mining.
- Four contract atom types: `symbol_use`, `private_symbol_use`, `error_regex`, and `json_shape_expectation`.
- CLI-first output as JSON, Markdown, and SARIF.
- Optional changed-only canary planning, dry-run by default.
- Artifact validation and release gates for tests, lint, typing, and build.

## Quick Start

Install for local development:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
```

Run the report flow:

```bash
python -m hyrumguard.cli init
python -m hyrumguard.cli discover demo_lib --config .hyrumguard.yml --out .hyrum/dependents.json
python -m hyrumguard.cli infer --from .hyrum/dependents.json --out .hyrum/shadow-contracts.lock.json
python -m hyrumguard.cli check --contracts .hyrum/shadow-contracts.lock.json --diff-file tests/fixtures/sample.diff --config .hyrumguard.yml --out .hyrum/risks.json
python -m hyrumguard.cli explain --risks .hyrum/risks.json --subject "missing token" --out .hyrum/explanation.md
python -m hyrumguard.cli report --risks .hyrum/risks.json --format markdown --out .hyrum/report.md
python -m hyrumguard.cli report --risks .hyrum/risks.json --format sarif --out hyrumguard.sarif
python -m hyrumguard.cli validate --dependents .hyrum/dependents.json --contracts .hyrum/shadow-contracts.lock.json --risks .hyrum/risks.json --sarif hyrumguard.sarif
python -m hyrumguard.cli canary --risks .hyrum/risks.json --dependents .hyrum/dependents.json --affected-only --out .hyrum/canary.json
```

The installed script exposes the same commands:

```bash
hyrumguard init
hyrumguard discover demo_lib --config .hyrumguard.yml
hyrumguard infer --from .hyrum/dependents.json
hyrumguard check --base origin/main --head HEAD
hyrumguard explain --subject "missing token"
hyrumguard report --format sarif --out hyrumguard.sarif
```

## Command Model

- `init`: writes a starter `.hyrumguard.yml` and refuses to overwrite without `--overwrite`.
- `discover`: collects manual seeds and optional ecosyste.ms dependent package data.
- `infer`: scans dependent repositories and writes `.hyrum/shadow-contracts.lock.json`.
- `check`: maps a git diff or explicit diff file to affected shadow contracts, with optional config-driven suppressions.
- `explain`: renders focused Markdown or JSON evidence for a risk selected by id or subject.
- `report`: renders the risk model as JSON, Markdown, or SARIF.
- `canary`: selects affected downstreams and defaults to a dry-run execution plan.
- `validate`: validates config, dependents, lockfile, risk JSON, and SARIF artifacts.

## Release Gates

Run these before cutting a local release:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m ruff check .
.venv/bin/python -m mypy hyrumguard
.venv/bin/python -m build
.venv/bin/python -m twine check dist/*
```

## Safety

HyrumGuard does not run third-party downstream tests by default. Canary execution requires both `--execute` and `--allow-unsafe-execution`, copies each dependent into a temporary directory, and enforces a timeout. HyrumGuard does not claim hard network isolation; use an external sandbox for untrusted code.

## Suppressions

Use suppressions for known and accepted findings. Suppressed risks stay in JSON, Markdown, and SARIF output with suppression metadata, while `summary.risk_count` counts only active unsuppressed risks.

```yaml
suppressions:
  - id: accepted-error-text
    subject: missing token
    type: error_regex
    reason: Accepted legacy client assertion while replacement ships.
    expires: 2099-12-31
```

## Explaining Risks

Use `explain` after `check` when you need one focused artifact for a finding:

```bash
hyrumguard explain --risks .hyrum/risks.json --subject "missing token"
hyrumguard explain --risks .hyrum/risks.json --id risk-contract-id --format json --out .hyrum/explanation.json
```

Explanations include the risk id, subject, type, severity, changed locations, dependents, evidence snippets, related contracts, and suppression state.

## Documentation

- [Architecture](docs/reference/architecture.md)
- [Configuration](docs/reference/configuration.md)
- [Contract atoms](docs/reference/contract-atoms.md)
- [Integrations](docs/reference/integrations.md)
- [Security and sandboxing](docs/reference/security-sandboxing.md)
- [Release process](docs/reference/release.md)
- [Roadmap](docs/reference/roadmap.md)
- [Pilot playbook](docs/reference/pilot-playbook.md)
- [Research source](docs/reference/research-report.md)
