# HyrumGuard Doctor Batch Plan

**Goal:** Add a local diagnostic command that summarizes config and artifact health for setup and CI readiness.

**Context:** Prior batches added suppressions, `init`, and targeted `explain`. The next useful stabilizer is an operational readiness command that wraps validation checks into a readable diagnostic report.

**Execution:** Work task-by-task. For production behavior, use TDD. After every completed task, run fresh verification and commit with the Lore Commit Protocol fallback format from `AGENTS.md`.

## Task 7: Open Doctor Batch

**Goal:** Replace the completed explainability batch plan/spec/control with the next measurable batch.

**Files:** `GOAL.md`, `SPEC.md`, `PLAN.md`, `CONTROL.md`, `ATTEMPTS.md`, `NOTES.md`

**Approach:** Keep previous evidence in `GOAL.md` progress and define the next batch around local diagnostics.

**Verification:** `git diff --check`

**Done when:** Durable state names doctor acceptance items and the task is committed.

## Task 8: Doctor Command

**Goal:** Add `hyrumguard doctor` for local diagnostic checks.

**Files to inspect:** `hyrumguard/cli.py`, `hyrumguard/validation.py`, `hyrumguard/io.py`, `tests/test_cli.py`, `tests/test_release_readiness.py`

**Approach:**

- Add failing tests for all-pass Markdown output, failed-check JSON output, CLI return codes, and concise error behavior.
- Add a small doctor module if it keeps CLI wiring thin.
- Reuse existing validation functions instead of duplicating schema logic.
- Keep `validate` behavior unchanged.

**Verification:**

- focused doctor tests
- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`
- `.venv/bin/python -m mypy hyrumguard`

**Done when:** Doctor behavior is tested, documented, and committed.

## Task 9: Batch Close

**Goal:** Prove the doctor batch did not regress the release baseline.

**Files:** codebase and distribution artifacts

**Approach:** Run full local gates and update working memory with evidence.

**Verification:**

- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`
- `.venv/bin/python -m mypy hyrumguard`
- `rm -rf dist build hyrumguard.egg-info && .venv/bin/python -m build`
- `.venv/bin/python -m twine check dist/*`
- CLI help smoke

**Done when:** Full gate evidence is recorded and committed, then the next batch is opened.
