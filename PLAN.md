# HyrumGuard Public Release Plan

**Goal:** Publish HyrumGuard as a stable public GitHub release `v1.0.0`.

**Context:** The local stable release candidate exists. Public release still needs public repo, commit, tag, remote push, GitHub Release, and verified release assets.

## Public Release Checklist

- [x] Inspect public-release prerequisites.
- [ ] Align goal/spec/docs/control with public-release scope.
- [ ] Add public-release readiness tests.
- [ ] Add tag-triggered release workflow and optional PyPI publishing boundary.
- [ ] Install/use `twine` and run `twine check`.
- [ ] Run full local gates.
- [ ] Commit release source with Lore Commit Protocol.
- [ ] Create public GitHub repo `BoSuY0/HyrumGuard` and set `origin`.
- [ ] Push default branch and tag `v1.0.0`.
- [ ] Create public GitHub Release `v1.0.0` with wheel/sdist assets.
- [ ] Verify public repo/release/assets from GitHub.
- [ ] Update `GOAL.md` evidence and complete the active goal only if public evidence passes.

## Task 1: Public Release Metadata

**Files:** `GOAL.md`, `SPEC.md`, `PLAN.md`, `CONTROL.md`, `README.md`, `pyproject.toml`, docs.

**Approach:** Replace local-only release framing with public GitHub release framing and actual repository URLs.

**Verification:** `pytest -q tests/test_public_release_readiness.py tests/test_release_readiness.py`

## Task 2: Automation And Gates

**Files:** `.github/workflows/release.yml`, `pyproject.toml`, tests.

**Approach:** Add release workflow and `twine` dev dependency/checks.

**Verification:** pytest, build, twine check.

## Task 3: Publish

**Files:** git history, GitHub repo, GitHub release.

**Approach:** Commit, tag, create public repo if missing, push, create release with assets.

**Verification:** `gh repo view`, `gh release view`, `gh release view --json assets`.
