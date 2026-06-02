# Attempts

## 2026-06-02

- Started from an empty git repository; no existing test command or package manager was present.
- Chose a Python stdlib-first CLI with pytest tests because the MVP needs Python AST support, JSON/SARIF output, and simple local execution without bootstrapping a Node project.
- RED attempt: `pytest -q` failed because `pytest` was not installed; created `.venv` and installed `.[dev]`.
- RED attempt: `.venv/bin/python -m pytest -q` then failed on missing `hyrumguard` modules, proving tests were ahead of production code.
- Focused GREEN: `.venv/bin/python -m pytest -q tests/test_mining.py tests/test_analysis_and_reports.py tests/test_cli.py` passed with `9 passed in 0.68s`.
- Full GREEN: `.venv/bin/python -m pytest -q` passed with `11 passed in 0.69s`.
- CLI smoke: all main and subcommand help commands exited 0.
- End-to-end smoke: discover wrote 1 dependent, infer wrote 8 shadow contracts, check wrote 5 risks, reports wrote Markdown and SARIF, canary wrote a dry-run plan for 1 dependent.
- Stable release RED: focused pytest failed on missing `validate`, missing `LICENSE`/`CHANGELOG`/`py.typed`, missing build dependency, old `__version__`, lack of unsafe canary acknowledgement, and timeout escaping as `TimeoutExpired`.
- Stable release GREEN: focused release tests passed with `10 passed`.
- Stable release gates: `.venv/bin/python -m pytest -q` passed with `18 passed`; `.venv/bin/python -m ruff check .` passed; `.venv/bin/python -m mypy hyrumguard` passed; `.venv/bin/python -m build` produced wheel and sdist.
- Stable fixture smoke: CLI help for all subcommands passed; fixture flow wrote 1 dependent, 8 contracts, 5 risks, Markdown, SARIF, validated 4 artifacts, and wrote dry-run canary for 1 dependent.
- Public release prerequisite audit: GitHub CLI is authenticated as `BoSuY0`; `BoSuY0/HyrumGuard` did not exist; repo had no commits/remotes/tags; `pip index versions hyrumguard` found no package; no PyPI/TWINE credentials were present.
- Public release RED: focused tests failed until project URLs, docs, workflow, and `twine` dependency were added.
- Public release GREEN: focused public-release tests passed with `11 passed`; full pytest passed with `22 passed`; ruff/mypy/build/twine/CLI help/fixture flow passed.
- Public publish: `gh repo create BoSuY0/HyrumGuard --public --source=. --remote=origin --push` succeeded and pushed `main`.
- Public publish: tag `v1.0.0` was pushed. The tag-triggered release workflow failed before steps/logs were available, so release assets were published manually with `gh release create v1.0.0 ... --verify-tag`.
- Public publish verification: GitHub API reported repo `BoSuY0/HyrumGuard` as `PUBLIC`; release `v1.0.0` is non-draft/non-prerelease and has wheel/sdist assets uploaded.
- Public CI verification: both public Actions runs failed before steps; check-run annotations report the account is locked due to a billing issue. This is an external account-state failure, not a code/test failure.
- Continuous hardening kickoff: reframed `GOAL.md`, `SPEC.md`, `PLAN.md`, and `CONTROL.md` from completed public-release state to a new batch covering suppressions, init, docs, and full local gates.
- Suppression RED: focused tests failed on multi-line YAML list mappings, missing config validation, missing analysis `suppressions` argument, canary selecting suppressed risks, and missing CLI `check --config`.
- Suppression GREEN: focused tests for suppression parsing, validation, analysis, reporters, canary filtering, and CLI config integration passed with `10 passed`.
- Suppression broader gates: full pytest passed with `32 passed`; `ruff check .` passed; `mypy hyrumguard` passed.
- Init RED: focused CLI tests failed because `init` was not a registered subcommand and overwrite protection did not exist.
- Init GREEN: focused CLI tests for help, default config, custom path, overwrite refusal, and explicit overwrite passed with `5 passed`.
- Init broader gates: full pytest passed with `36 passed`; `ruff check .` passed; `mypy hyrumguard` passed.
- Batch close gates: build succeeded, `twine check dist/*` passed, CLI help smoke returned `all-help-ok 8`, and fixture flow with generated starter config wrote 5 active risks, 0 suppressions, and 1 canary selection.
- Explainability batch kickoff: selected targeted risk explanation as the next user-visible workflow after suppression/init hardening.
- Explain RED: focused tests failed at collection because `hyrumguard.explain` did not exist and CLI `explain` was not registered.
- Explain GREEN: focused tests for subject/id selection, Markdown/JSON rendering, `--out`, help, and missing-match errors passed with `7 passed`.
- Explain broader gates: full pytest passed with `42 passed`; `ruff check .` passed; `mypy hyrumguard` passed.
- Explain batch close gates: build succeeded, `twine check dist/*` passed, CLI help smoke returned `all-help-ok 9`, and fixture flow wrote Markdown/JSON explain artifacts with one matched explanation.
- Doctor batch kickoff: selected local diagnostics as the next operational-readiness workflow.
