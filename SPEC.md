# HyrumGuard Continuous Hardening Specification

## Goal

Keep HyrumGuard moving beyond the public `v1.0.0` release by adding concrete user-visible functionality, increasing regression coverage, and tightening architecture in small verified commits.

The current batch adds:

1. Risk suppressions for known/accepted Hyrum's Law findings.
2. A first-run initializer for starter configuration.
3. Documentation updates that describe the new flows and preserve safety boundaries.

## Product Baseline

HyrumGuard is a local CLI/package for:

- downstream discovery
- implicit usage mining
- shadow contract synthesis
- PR-time risk analysis
- changed-only canary planning
- JSON, Markdown, and SARIF output
- artifact validation

It supports Python and JavaScript/TypeScript downstream mining for PyPI/npm-style projects. Canary execution remains dry-run by default.

## Current Batch Requirements

### CB-1 Risk Suppressions

Users can define suppressions in `.hyrumguard.yml` for risks they knowingly accept. A suppression must be explicit and auditable.

Required behavior:

- Suppressions are loaded from config.
- Each suppression can target a risk by stable risk id, subject, or contract type.
- Suppressed risks remain visible in machine output with suppression metadata instead of disappearing silently.
- Markdown reports summarize active suppressions.
- SARIF output marks suppressed findings with SARIF suppression metadata when possible.
- Validation rejects malformed suppression entries.
- Expired suppressions are ignored or reported as expired, with tests covering the behavior.

### CB-2 First-Run Initialization

Users can run a CLI command to create a starter `.hyrumguard.yml`.

Required behavior:

- The command writes a useful starter config in the current directory by default.
- It refuses to overwrite an existing file unless an explicit overwrite flag is provided.
- It supports writing to a custom path.
- It is covered by CLI tests.

### CB-3 Documentation And Structure

Docs should explain:

- how suppressions work
- how to initialize a config
- what remains unsafe or out of scope
- where generated outputs belong

## Non-Goals

- No hosted service.
- No app backend.
- No new ecosystems beyond the existing Python and JavaScript/TypeScript slice.
- No silent dropping of findings.
- No weakening of unsafe canary acknowledgement.
- No PyPI publication unless separately approved and verified.

## Scorecard

For each task:

- focused tests prove the new behavior
- shared gates run when touched code affects CLI, validation, reporting, or analysis
- docs are updated for user-visible behavior
- a commit records the completed task

Batch close requires:

- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`
- `.venv/bin/python -m mypy hyrumguard`
- `rm -rf dist build hyrumguard.egg-info && .venv/bin/python -m build`
- `.venv/bin/python -m twine check dist/*`
- CLI help smoke

## Human Control

The user controls the stop point. After this batch is complete, Codex should open the next focused batch instead of calling the goal complete.
