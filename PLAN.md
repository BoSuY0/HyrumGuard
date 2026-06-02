# HyrumGuard Continuous Hardening Plan

**Goal:** Add real functionality, broad tests, and architecture stabilization in small verified commits.

**Context:** Public release `v1.0.0` exists. The next work should improve day-two usability and maintainability without expanding the product into hosted services or new ecosystems.

**Execution:** Work task-by-task. For production behavior, use TDD. After every completed task, run fresh verification and commit with the Lore Commit Protocol fallback format from `AGENTS.md`.

## Task 0: Reframe Goal State

**Goal:** Replace the completed public-release goal state with a continuous hardening contract.

**Files:** `GOAL.md`, `SPEC.md`, `PLAN.md`, `CONTROL.md`, `ATTEMPTS.md`, `NOTES.md`

**Approach:** Keep the public release evidence as historical context, then define the current batch and stop rules.

**Verification:** `git diff --check`

**Done when:** Durable state names the current batch and the task is committed.

## Task 1: Risk Suppression Policy

**Goal:** Let users suppress known risks from config while keeping audit evidence visible.

**Files to inspect:** `hyrumguard/config.py`, `hyrumguard/analysis.py`, `hyrumguard/reporters/json.py`, `hyrumguard/reporters/markdown.py`, `hyrumguard/reporters/sarif.py`, `hyrumguard/validation.py`, `hyrumguard/cli.py`, `tests/*`

**Approach:**

- Add failing tests for suppression loading, analysis/report output, validation, and CLI integration.
- Add a typed suppression model or helper module if it reduces duplication.
- Apply suppressions after risk detection so generated evidence remains auditable.
- Keep unsuppressed-risk behavior unchanged.

**Verification:**

- focused suppression tests
- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`
- `.venv/bin/python -m mypy hyrumguard`

**Done when:** Suppression behavior is tested, documented, and committed.

## Task 2: First-Run Init Command

**Goal:** Add a safe CLI initializer for starter `.hyrumguard.yml` files.

**Files to inspect:** `hyrumguard/cli.py`, `hyrumguard/config.py`, `README.md`, `docs/reference/configuration.md`, `tests/test_cli.py`

**Approach:**

- Add failing CLI tests for default output, custom path, and overwrite protection.
- Implement `hyrumguard init` with explicit overwrite semantics.
- Document the command and starter config shape.

**Verification:**

- focused CLI tests
- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`

**Done when:** Init behavior is tested, documented, and committed.

## Task 3: Batch Close

**Goal:** Prove the hardening batch did not regress the release baseline.

**Files:** codebase and distribution artifacts

**Approach:** Run full local gates and update working memory with the evidence.

**Verification:**

- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`
- `.venv/bin/python -m mypy hyrumguard`
- `rm -rf dist build hyrumguard.egg-info && .venv/bin/python -m build`
- `.venv/bin/python -m twine check dist/*`
- CLI help smoke

**Done when:** Full gate evidence is recorded and the batch close is committed.
