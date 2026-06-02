# HyrumGuard v0.1 Execution Plan

**Goal:** Implement the approved v0.1 design as a tested CLI and documentation set.

## Task A: RED Tests

**Goal:** Lock the MVP behavior before production code.

**Files:** `tests/test_mining.py`, `tests/test_analysis_and_reports.py`, `tests/test_cli.py`, fixture downstream repositories.

**Approach:** Assert atom extraction, lockfile synthesis, diff risk mapping, canary dry-run planning, reporter output, and CLI help.

**Verification:** `pytest -q` fails for missing implementation before production code is added.

**Done when:** The failure is for missing `hyrumguard` modules, not malformed tests.

## Task B: Core Models And Config

**Goal:** Provide deterministic data structures and config loading.

**Files:** `hyrumguard/models.py`, `hyrumguard/config.py`

**Approach:** Use dataclasses with stable IDs and `to_dict` helpers. Support JSON and a small YAML subset for `.hyrumguard.yml`.

**Verification:** Config and model tests pass.

## Task C: Mining And Synthesis

**Goal:** Extract and cluster the four v0.1 atom types.

**Files:** `hyrumguard/miners/**`, `hyrumguard/synthesis.py`

**Approach:** Use Python AST for imports/private access and line regexes for behavior expectations; use JS/TS regexes for imports, requires, error regexes, and JSON key expectations.

**Verification:** `pytest -q tests/test_mining.py`

## Task D: Analysis, Canary, Reporters

**Goal:** Turn lockfiles and diffs into maintainer-facing risk output.

**Files:** `hyrumguard/diff.py`, `hyrumguard/analysis.py`, `hyrumguard/canary.py`, `hyrumguard/reporters/**`

**Approach:** Parse unified diff text, derive changed subjects, match contracts, select affected downstreams, and render JSON/Markdown/SARIF.

**Verification:** `pytest -q tests/test_analysis_and_reports.py`

## Task E: CLI And Docs

**Goal:** Expose the report's command flow and document it.

**Files:** `hyrumguard/cli.py`, `README.md`, `docs/reference/**`, `examples/**`, `action.yml`, `.github/workflows/hyrumguard.yml`

**Approach:** Implement argparse subcommands and examples that use the same file names as the report.

**Verification:** `pytest -q tests/test_cli.py` and CLI help commands.
