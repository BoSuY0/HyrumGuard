# HyrumGuard Public Release Specification

## Goal

Finish HyrumGuard as a stable public release. The concrete release target is a public GitHub repository and non-draft GitHub Release `v1.0.0` containing verified Python wheel and source distribution assets.

The release remains a local CLI/package product. PyPI publication is desirable, but it must not be claimed unless a real upload succeeds and is verified.

## Public Release Scope

- Public repository: `https://github.com/BoSuY0/HyrumGuard`
- Public release: `v1.0.0`
- Release assets:
  - `hyrumguard-1.0.0.tar.gz`
  - `hyrumguard-1.0.0-py3-none-any.whl`
- Package name: `hyrumguard`
- Product: CLI for downstream discovery, shadow contract mining, PR risk reporting, validation, and changed-only canary planning.

## Non-Goals

- No hosted SaaS.
- No full GitHub App or GitLab App backend.
- No languages/ecosystems beyond Python and JavaScript/TypeScript, npm/PyPI.
- No claim of PyPI upload without real PyPI/TestPyPI credentials or trusted-publisher proof.
- No claim of hard network sandboxing inside HyrumGuard itself.

## Required Capabilities

1. Public release metadata
   - Project URLs point to the public repo.
   - README/docs mention the public release channel.
   - Changelog has `1.0.0`.

2. Public release automation
   - GitHub Actions validates tests, lint, type checks, build, smoke, and artifact validation.
   - Tag-triggered release workflow builds wheel/sdist, runs `twine check`, uploads GitHub Release assets, and documents optional PyPI publishing.

3. Local gates
   - Pytest, ruff, mypy, build, twine check, CLI help, and fixture flow pass.

4. Published state
   - Source is committed, pushed, and visible in public repo.
   - Tag `v1.0.0` is pushed.
   - Public GitHub Release `v1.0.0` exists with both distribution assets.

## Scorecard

Completion requires:

- every local gate passes
- `gh repo view BoSuY0/HyrumGuard` proves the repo is public
- `gh release view v1.0.0 --repo BoSuY0/HyrumGuard` proves the release is public, non-draft, and non-prerelease
- release assets list includes both built artifacts

## Fast Feedback Loop

Run `.venv/bin/python -m pytest -q tests/test_public_release_readiness.py tests/test_release_readiness.py` after release metadata/workflow edits.
