# Stable Release Implementation Plan

**Goal:** Execute the stable-release plan without losing the existing product flow.

## Task 1: Contract Alignment

**Goal:** Replace v0.1-only durable state with stable-release state.

**Files:** `GOAL.md`, `SPEC.md`, `PLAN.md`, `CONTROL.md`, stable release plan docs.

**Verification:** Read files and confirm they agree on scope and non-goals.

## Task 2: Release Readiness Tests

**Goal:** Add failing tests for release-grade behavior before code changes.

**Files:** `tests/test_release_readiness.py`, `tests/test_cli.py`, `tests/test_config_and_discovery.py`

**Verification:** Focused pytest fails for missing `validate`, metadata, and friendly error behavior.

## Task 3: Validation And CLI Hardening

**Goal:** Add artifact validators and stable CLI error behavior.

**Files:** `hyrumguard/validation.py`, `hyrumguard/cli.py`

**Verification:** Focused pytest passes.

## Task 4: Packaging And Quality Gates

**Goal:** Make the project buildable and quality-checkable.

**Files:** `pyproject.toml`, `LICENSE`, `CHANGELOG.md`, `hyrumguard/py.typed`, CI workflow.

**Verification:** build, ruff, mypy, pytest.

## Task 5: Release Docs And Final Smoke

**Goal:** Ensure users can run and release the tool from docs.

**Files:** `README.md`, `docs/reference/release.md`, existing reference docs.

**Verification:** CLI help smoke and fixture flow.
