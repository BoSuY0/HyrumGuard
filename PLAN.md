# HyrumGuard Explainability Batch Plan

**Goal:** Add a risk explanation workflow so maintainers can inspect one finding without manually reading raw JSON.

**Context:** The first continuous hardening batch added suppressions, `init`, docs, and full gate evidence. The next useful day-two workflow is targeted explanation of existing risk artifacts.

**Execution:** Work task-by-task. For production behavior, use TDD. After every completed task, run fresh verification and commit with the Lore Commit Protocol fallback format from `AGENTS.md`.

## Task 4: Open Explainability Batch

**Goal:** Replace the completed first-batch plan/spec/control with the next measurable batch.

**Files:** `GOAL.md`, `SPEC.md`, `PLAN.md`, `CONTROL.md`, `ATTEMPTS.md`, `NOTES.md`

**Approach:** Keep first-batch evidence in `GOAL.md` progress and define the next batch around risk explanation.

**Verification:** `git diff --check`

**Done when:** Durable state names explainability acceptance items and the task is committed.

## Task 5: Risk Explain Command

**Goal:** Add `hyrumguard explain` for targeted risk inspection.

**Files to inspect:** `hyrumguard/cli.py`, `hyrumguard/reporters/*`, `hyrumguard/io.py`, `tests/test_cli.py`, `tests/test_analysis_and_reports.py`, `tests/test_suppressions.py`

**Approach:**

- Add failing tests for matching by risk id, matching by subject, Markdown output, JSON output, `--out`, and missing-match errors.
- Add a small explanation module if it keeps CLI wiring thin.
- Render suppressed risks explicitly, including suppression id/reason.
- Keep existing `report` output unchanged.

**Verification:**

- focused explain tests
- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`
- `.venv/bin/python -m mypy hyrumguard`

**Done when:** Explain behavior is tested, documented, and committed.

## Task 6: Batch Close

**Goal:** Prove the explainability batch did not regress the release baseline.

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
