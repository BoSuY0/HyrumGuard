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
