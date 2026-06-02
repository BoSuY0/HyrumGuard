<goal>
Continuously harden HyrumGuard with user-visible functionality, broad regression tests, and cleaner architecture until the user explicitly ends the loop. The current batch focuses on local operational readiness diagnostics.
</goal>

<context>
Canonical inputs:
- `/home/tetra/Downloads/deep-research-report.md`
- `AGENTS.md`
- `SPEC.md`
- `PLAN.md`
- `CONTROL.md`
- `README.md`
- `docs/reference/*`

Current product baseline:
- Public repo: `https://github.com/BoSuY0/HyrumGuard`
- Public release: `v1.0.0`
- Package version: `1.0.0`
- Existing CLI commands: `init`, `discover`, `infer`, `check`, `explain`, `canary`, `report`, `validate`
- Existing local gates: pytest, ruff, mypy, build, twine check, CLI help smoke, fixture smoke flow
- Public GitHub Actions are blocked by an external billing lock before jobs start; local gates remain the trusted feedback loop until the account state is fixed.
- No Graphify artifacts or callable Graphify MCP tools are currently available in this repo; normal repo inspection is the fallback.

Useful commands:
- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`
- `.venv/bin/python -m mypy hyrumguard`
- `.venv/bin/python -m build`
- `.venv/bin/python -m twine check dist/*`
- `.venv/bin/python -m hyrumguard.cli --help`
- `git status --short --branch`
</context>

<constraints>
- Respond to the user in Ukrainian.
- Follow `AGENTS.md` and the invoked goal skills.
- Use TDD for production feature work: failing test first, targeted green, then broader gates.
- Use `apply_patch` for manual edits.
- Commit after each completed task or TODO using the Lore Commit Protocol fallback from `AGENTS.md`.
- Preserve unrelated user changes and keep generated runtime outputs out of git.
- Do not add hosted services, GitHub App backends, GitLab App backends, or new language ecosystems without explicit approval.
- Canary execution remains dry-run by default; real downstream execution still requires explicit unsafe acknowledgement.
- Do not call `update_goal complete` while the user has asked the loop to continue. Complete only after the user explicitly ends the work and the latest accepted batch has fresh verification evidence.
</constraints>

<scorecard>
Primary score: committed, verified improvement tasks per batch.

Passing threshold for each task:
- At least one observable product, architecture, documentation, or test outcome is completed.
- Relevant focused tests pass in the current repo state.
- Broader regression gates run when the change can affect shared behavior.
- A Lore-style commit exists after the task.

Current batch acceptance:
- DB-0 Goal-loop state names the doctor batch and is committed.
- DB-1 `hyrumguard doctor` checks selected config/artifact paths and renders Markdown/JSON diagnostics.
- DB-2 Docs describe the diagnostic workflow and architecture boundaries.
- DB-3 Full local gates pass after the batch.

Stop condition: keep opening the next small batch after DB-3 unless the user explicitly tells Codex to stop or finish.
</scorecard>

<done_when>
- [ ] DB-0 Durable goal/spec/plan/control state reflects doctor batch scope and is committed.
- [ ] DB-1 CLI `doctor` renders selected config/artifact diagnostics in Markdown and JSON.
- [ ] DB-2 Docs explain local diagnostics and current architecture boundaries.
- [ ] DB-3 Batch regression gates pass: pytest, ruff, mypy, build, twine check, and CLI smoke.
</done_when>

<feedback_loop>
Fast checks:
- Focused pytest for the feature under development.
- `.venv/bin/python -m ruff check .`

Expected runtime: focused tests under 10 seconds, full local gates under a few minutes.

Cadence:
- Run RED before implementation for production features.
- Run focused GREEN before each task commit.
- Run full gates after shared architecture or CLI changes and at batch close.
</feedback_loop>

<workflow>
1. Re-read `GOAL.md`, `AGENTS.md`, `SPEC.md`, `PLAN.md`, and `CONTROL.md`.
2. Pick the next unchecked current-batch item.
3. Inspect the real source and tests before naming integration points.
4. For production behavior, write the failing test first and verify it fails for the intended reason.
5. Implement the smallest coherent change, then run focused tests.
6. Update docs and working memory where the task changes user-visible behavior.
7. Run verification appropriate to the blast radius.
8. Commit that task with a Lore Commit Protocol fallback message.
9. Update Progress and continue to the next task.
</workflow>

<working_memory>
Maintain:
- `GOAL.md` as the canonical goal-loop state tracker.
- `SPEC.md` as the current product/batch specification.
- `PLAN.md` as the executable task list.
- `ATTEMPTS.md` as the compact evidence log for experiments, failures, and gate outcomes.
- `NOTES.md` as durable observations and decisions.
- `CONTROL.md` as the user-visible knobs and stop/pivot gates.
</working_memory>

<human_control_surface>
The user controls when this continuous loop ends. Until then, prefer small verified tasks and commits over a single giant refactor.

Require explicit new approval before:
- publishing to PyPI/TestPyPI
- adding hosted services or app backends
- adding more language ecosystems
- making canary execution blocking by default
- deleting public release artifacts or rewriting published history
</human_control_surface>

<verification_loop>
Focused:
- Run the nearest relevant pytest file for each task.

Batch close:
- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`
- `.venv/bin/python -m mypy hyrumguard`
- `rm -rf dist build hyrumguard.egg-info && .venv/bin/python -m build`
- `.venv/bin/python -m twine check dist/*`
- CLI help smoke for every subcommand
</verification_loop>

<execution_rules>
- Check git status before edits.
- Preserve unrelated user changes.
- Prefer `rg` over `grep`.
- Use `apply_patch` for manual edits.
- Use TDD for feature work.
- Before claiming a task is complete, run fresh verification.
- After each completed task, commit.
- Keep final communication concise and in Ukrainian.
</execution_rules>

<output_contract>
Interim responses should report the current task, commit hash, and verification evidence. Final completion is user-controlled; do not call the goal complete while the user is still asking for more work.
</output_contract>

## Progress

### Completed

- 2026-06-02, prior public-release goal completed. evidence: public repo `BoSuY0/HyrumGuard`, tag/release `v1.0.0`, verified wheel/sdist assets, local gates passed, public CI caveat documented.
- 2026-06-02, CB-0 verified. evidence: commit `ef2f950` reframed `GOAL.md`, `SPEC.md`, `PLAN.md`, `CONTROL.md`, `ATTEMPTS.md`, and `NOTES.md`; `git diff --check` passed.
- 2026-06-02, CB-1 verified. evidence: suppression RED failed for missing parser/validator/analysis/canary/CLI behavior; GREEN passed with focused `10 passed`, full pytest `32 passed`, ruff clean, mypy clean.
- 2026-06-02, CB-2 verified. evidence: `hyrumguard init` tests covered help/default config/custom path/overwrite refusal/explicit overwrite; full pytest `36 passed`, ruff clean, mypy clean.
- 2026-06-02, CB-3 verified. evidence: `README.md`, `docs/reference/configuration.md`, and `docs/reference/architecture.md` document suppressions, init, and safety/architecture boundaries.
- 2026-06-02, CB-4 verified. evidence: pytest `36 passed`; ruff clean; mypy clean; build created wheel/sdist; twine check PASSED; CLI help smoke `all-help-ok 8`; fixture flow with `init --path` and `check --config` exited 0.
- 2026-06-02, EB-0 verified. evidence: commit `903e4b7` opened explainability batch in `GOAL.md`, `SPEC.md`, `PLAN.md`, `CONTROL.md`, `ATTEMPTS.md`, and `NOTES.md`; `git diff --check` passed.
- 2026-06-02, EB-1 verified. evidence: focused explain tests passed with `7 passed`; full pytest `42 passed`; ruff clean; mypy clean.
- 2026-06-02, EB-2 verified. evidence: `README.md` documents `explain`; `docs/reference/architecture.md` includes `hyrumguard.explain` and the risk explainer data-flow step.
- 2026-06-02, EB-3 verified. evidence: pytest `42 passed`; ruff clean; mypy clean; build created wheel/sdist; twine check PASSED; CLI help smoke `all-help-ok 9`; fixture flow with Markdown/JSON explain artifacts exited 0.

### In Progress

- 2026-06-02, DB-0 in progress. Bridge: define doctor batch state, commit it, then start RED tests for `hyrumguard doctor`.

### Blockers / Open Questions

- External CI caveat: GitHub Actions jobs cannot start while the GitHub account is locked due to a billing issue.
- Active Codex goal tool state is paused, but the user explicitly resumed work in chat; continue working from `GOAL.md` and do not mark complete.

### Iteration Log

- 2026-06-02, Started continuous hardening loop from a clean `main...origin/main` state after public release evidence commit `26799cd`.
- 2026-06-02, First continuous hardening batch closed at commit `5b3fd2f`; next batch selected for targeted risk explainability.
- 2026-06-02, Explain RED failed on missing `hyrumguard.explain` module; GREEN focused explain suite passed with `7 passed`.
- 2026-06-02, Explainability batch closed locally; next batch should improve operational readiness.
- 2026-06-02, Doctor batch selected to improve local setup and CI-readiness diagnostics.
