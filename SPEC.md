# HyrumGuard Continuous Hardening Specification

## Goal

Keep HyrumGuard moving beyond the public `v1.0.0` release by adding concrete user-visible functionality, increasing regression coverage, and tightening architecture in small verified commits.

The current batch improves operational readiness: maintainers should be able to run one diagnostic command that checks local config and artifact health before wiring HyrumGuard into CI.

## Product Baseline

HyrumGuard is a local CLI/package for:

- first-run configuration initialization
- downstream discovery
- implicit usage mining
- shadow contract synthesis
- PR-time risk analysis with auditable suppressions
- targeted risk explanation
- changed-only canary planning
- JSON, Markdown, and SARIF output
- artifact validation

It supports Python and JavaScript/TypeScript downstream mining for PyPI/npm-style projects. Canary execution remains dry-run by default.

## Current Batch Requirements

### DB-1 Doctor Command

Users can run a local diagnostic command before using HyrumGuard in CI.

Required behavior:

- The CLI exposes `hyrumguard doctor`.
- The command can check selected config and artifact paths.
- It reports each check as pass/fail with a concise message.
- It supports Markdown output by default and JSON output for automation.
- It returns success when all selected checks pass and non-zero when any selected check fails.
- It does not throw tracebacks for malformed inputs unless `--debug` is used.
- It is covered by focused unit/CLI tests.

### DB-2 Documentation And Architecture

Docs should explain:

- when to use `doctor` versus `validate`
- how JSON doctor output can be consumed by CI
- that `doctor` is local-only and does not run downstream code

### DB-3 Batch Close

The batch closes only after full local gates pass.

## Non-Goals

- No hosted service.
- No app backend.
- No new ecosystems beyond the existing Python and JavaScript/TypeScript slice.
- No live dependency fetching inside `doctor`.
- No downstream test execution inside `doctor`.
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
