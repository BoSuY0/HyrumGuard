<goal>
Finish HyrumGuard as a stable public release: a public GitHub repository `BoSuY0/HyrumGuard` with committed source, passing release gates, tag `v1.0.0`, a public GitHub Release containing the verified wheel and sdist assets, and documentation/automation that makes future PyPI publication explicit without falsely claiming PyPI upload when credentials are unavailable.
</goal>

<context>
Canonical inputs:
- `/home/tetra/Downloads/deep-research-report.md`
- `SPEC.md`
- `README.md`
- `AGENTS.md`
- `PLAN.md`
- `CONTROL.md`

Current evidence observed on 2026-06-02:
- GitHub CLI is installed and authenticated as active account `BoSuY0` with `repo` and `workflow` scopes.
- `gh repo view BoSuY0/HyrumGuard` and `BoSuY0/hyrumguard` did not resolve, so the target repo name appears available.
- Local repo has no commits, no tags, and no remote before public-release work.
- `pip index versions hyrumguard` returned `No matching distribution found for hyrumguard`; this is only a package-name availability signal, not PyPI publication.
- `twine` was not installed before public-release work.
- No Graphify artifacts or callable Graphify MCP tools were available; normal repo inspection is the fallback.

Useful commands:
- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`
- `.venv/bin/python -m mypy hyrumguard`
- `.venv/bin/python -m build`
- `.venv/bin/python -m twine check dist/*`
- `.venv/bin/python -m hyrumguard.cli --help`
- `git status --short --branch`
- `gh repo view BoSuY0/HyrumGuard --json nameWithOwner,visibility,url`
- `gh release view v1.0.0 --repo BoSuY0/HyrumGuard --json tagName,url,isDraft,isPrerelease`
</context>

<constraints>
- Public release is GitHub-public by default: source repository plus GitHub Release assets. Do not claim PyPI publication unless a real PyPI/TestPyPI upload succeeds and is verified.
- Preserve the research report's core product: downstream discovery, implicit usage mining, shadow contracts, PR-time risk analysis, changed-only canary, and maintainer-facing reports.
- Do not add hosted service, GitHub App backend, GitLab App backend, or new language ecosystems.
- Canary execution remains dry-run by default. Real downstream execution requires explicit unsafe acknowledgement.
- Keep generated runtime outputs out of git. `dist/` stays ignored and is uploaded as release assets, not committed.
- Use the Lore Commit Protocol for commits; no local `docs/lore-commit-protocol.md` exists, so use the fallback format from `AGENTS.md`.
</constraints>

<scorecard>
Primary score: public-release acceptance checklist below.

Passing threshold:
- Every `done_when` item is checked with evidence in Progress.
- Local release gates pass.
- Public GitHub repository is visible.
- Public GitHub release `v1.0.0` is visible and has wheel/sdist assets.

Regression checks:
- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`
- `.venv/bin/python -m mypy hyrumguard`
- `rm -rf dist build hyrumguard.egg-info && .venv/bin/python -m build`
- `.venv/bin/python -m twine check dist/*`
- CLI help smoke for all subcommands
- fixture smoke flow with `validate`
- `gh repo view BoSuY0/HyrumGuard --json nameWithOwner,visibility,url`
- `gh release view v1.0.0 --repo BoSuY0/HyrumGuard --json tagName,url,isDraft,isPrerelease`

Stop condition: call `update_goal complete` only when the public release evidence proves every item.
</scorecard>

<done_when>
- [x] PR-0.1 Stable local release candidate exists with passing tests, lint, type check, build, CLI help, fixture flow, and wheel/sdist artifacts.
- [x] PR-1.1 `GOAL.md`, `SPEC.md`, `PLAN.md`, `CONTROL.md`, `README.md`, and release docs describe stable public GitHub release scope and PyPI boundary consistently.
- [x] PR-1.2 Project metadata URLs point to the actual public repository `https://github.com/BoSuY0/HyrumGuard`.
- [x] PR-1.3 Release automation exists for tag-triggered GitHub release asset upload and documented optional PyPI publication.
- [x] PR-2.1 Public-release readiness tests cover metadata URLs, release docs, release workflow, twine check prerequisites, and existing stable product gates.
- [x] PR-2.2 Final local gates pass: pytest, ruff, mypy, build, twine check, CLI help, fixture flow.
- [ ] PR-3.1 Initial release commit exists with Lore Commit Protocol message.
- [ ] PR-3.2 Public GitHub repository `BoSuY0/HyrumGuard` exists, is public, and local `origin` points to it.
- [ ] PR-3.3 Default branch is pushed to the public GitHub repository.
- [ ] PR-3.4 Tag `v1.0.0` exists locally and remotely at the release commit.
- [ ] PR-3.5 Public GitHub Release `v1.0.0` exists, is not draft, is not prerelease, and includes `hyrumguard-1.0.0.tar.gz` and `hyrumguard-1.0.0-py3-none-any.whl`.
- [ ] PR-4.1 Completion audit verifies public URLs and release assets from GitHub, not only local files.
</done_when>

<feedback_loop>
Fast check: `.venv/bin/python -m pytest -q tests/test_public_release_readiness.py tests/test_release_readiness.py`
Expected runtime: under 10 seconds.
Cadence: after metadata/docs/workflow edits.
Final check: run every scorecard command before committing, and verify GitHub repo/release after publishing.
</feedback_loop>

<workflow>
1. Re-read `GOAL.md`, `AGENTS.md`, `SPEC.md`, `PLAN.md`, `CONTROL.md`.
2. Add tests and docs for public release readiness.
3. Update metadata/workflows/docs until tests pass.
4. Run full local release gates and rebuild `dist/`.
5. Commit with Lore Commit Protocol.
6. Create public GitHub repo if missing, set remote, push branch and tag.
7. Create public GitHub Release `v1.0.0` with wheel/sdist assets.
8. Verify public repo/release through `gh` and, if needed, web URLs.
9. Update Progress evidence and complete only when public evidence proves every item.
</workflow>

<working_memory>
Maintain:
- `PLAN.md`
- `ATTEMPTS.md`
- `NOTES.md`
- `CONTROL.md`

Update after failed gates, publishing actions, blockers, and completion audit.
</working_memory>

<human_control_surface>
`CONTROL.md` lists publish knobs. Public GitHub release is authorized by the active objective. PyPI/TestPyPI upload requires real credentials or trusted-publisher configuration; do not fake it.
</human_control_surface>

<verification_loop>
Focused:
- `.venv/bin/python -m pytest -q tests/test_public_release_readiness.py tests/test_release_readiness.py`

Final:
- `.venv/bin/python -m pytest -q`
- `.venv/bin/python -m ruff check .`
- `.venv/bin/python -m mypy hyrumguard`
- `rm -rf dist build hyrumguard.egg-info && .venv/bin/python -m build`
- `.venv/bin/python -m twine check dist/*`
- CLI help smoke
- fixture smoke flow with validation
- `gh repo view BoSuY0/HyrumGuard --json nameWithOwner,visibility,url`
- `gh release view v1.0.0 --repo BoSuY0/HyrumGuard --json tagName,url,isDraft,isPrerelease`
</verification_loop>

<execution_rules>
- Check git status before edits.
- Preserve unrelated user changes.
- Prefer `rg` over `grep`.
- Use `apply_patch` for manual edits.
- Use TDD for release-readiness behavior.
- Do not publish to PyPI without real credentials and evidence.
- Do not mark complete if public repo or public release cannot be verified.
- Keep final communication concise and in Ukrainian.
</execution_rules>

<output_contract>
Final response should include public repository URL, public release URL, release asset names, verification commands, and goal usage after `update_goal complete`.
</output_contract>

## Progress

### Completed

- 2026-06-02, PR-0.1 verified. evidence: prior stable local release gate passed; `dist/` contains wheel/sdist.
- 2026-06-02, PR-1.1 verified. evidence: `GOAL.md`, `SPEC.md`, `PLAN.md`, `CONTROL.md`, `README.md`, `docs/reference/release.md` describe public GitHub release and PyPI boundary.
- 2026-06-02, PR-1.2 verified. evidence: `pyproject.toml` URLs point to `https://github.com/BoSuY0/HyrumGuard`.
- 2026-06-02, PR-1.3 verified. evidence: `.github/workflows/release.yml` builds, runs `twine check`, uploads GitHub Release assets, and keeps PyPI job opt-in.
- 2026-06-02, PR-2.1 verified. evidence: `tests/test_public_release_readiness.py` and `tests/test_release_readiness.py`; focused suite -> `11 passed`.
- 2026-06-02, PR-2.2 verified. evidence: pytest -> `22 passed`; ruff/mypy -> clean; build+twine -> PASSED; CLI help -> `all-help-ok`; fixture flow exited 0.

### In Progress

- 2026-06-02, Bridge: current work feeds PR-3.1 through PR-3.5; output enters public release state when source, tag, and GitHub Release are visible at `BoSuY0/HyrumGuard`.

### Blockers / Open Questions

- Potential PyPI blocker: no `TWINE_*`/`PYPI_*` credentials were present; public GitHub release is the verified public-release channel unless credentials appear.

### Iteration Log

- 2026-06-02 18:00, Inspected public-release prerequisites: GitHub auth exists, repo name appears available, no remote/commits/tags exist, PyPI name appears unused, twine missing. next: add public-release metadata/docs/workflow/tests.
- 2026-06-02 18:10, Added public-release docs/tests/workflow, updated URLs to `BoSuY0/HyrumGuard`, installed twine, and passed local public-release gates. next: commit, push, tag, and create GitHub Release.
