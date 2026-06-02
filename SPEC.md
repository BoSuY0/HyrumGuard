# HyrumGuard Continuous Hardening Specification

## Goal

Keep HyrumGuard moving beyond the public `v1.0.0` release by adding concrete user-visible functionality, increasing regression coverage, and tightening architecture in small verified commits.

The current batch improves explainability: maintainers should be able to inspect a specific risk without manually digging through `.hyrum/risks.json`.

## Product Baseline

HyrumGuard is a local CLI/package for:

- first-run configuration initialization
- downstream discovery
- implicit usage mining
- shadow contract synthesis
- PR-time risk analysis with auditable suppressions
- changed-only canary planning
- JSON, Markdown, and SARIF output
- artifact validation

It supports Python and JavaScript/TypeScript downstream mining for PyPI/npm-style projects. Canary execution remains dry-run by default.

## Current Batch Requirements

### EB-1 Risk Explanation Command

Users can explain one or more risks from a generated risk artifact.

Required behavior:

- The CLI exposes `hyrumguard explain`.
- Users can select risks by `--id` or `--subject`.
- The command defaults to Markdown and can emit JSON.
- The command includes severity, type, subject, reason, dependents, changed locations, suppression state, and evidence snippets.
- Missing matches return a concise non-traceback error.
- The command supports `--out` for writing the explanation artifact.
- It is covered by focused unit/CLI tests.

### EB-2 Documentation And Architecture

Docs should explain:

- how `explain` fits after `check`
- which fields are included in the explanation
- how suppressed risks are shown
- how this differs from full reports

### EB-3 Batch Close

The batch closes only after full local gates pass.

## Non-Goals

- No hosted service.
- No app backend.
- No new ecosystems beyond the existing Python and JavaScript/TypeScript slice.
- No live dependency fetching inside `explain`.
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
