# Stable Release Design

## Observed Facts

- The repository has a v0.1 HyrumGuard CLI with tests and docs.
- Current active objective asks for the whole project to reach a stable release.
- Existing `GOAL.md`, `SPEC.md`, `README.md`, and `CONTROL.md` were v0.1-oriented and needed widening.

## Stable Release Interpretation

Stable release means a publishable local CLI/package release candidate. It does not mean a hosted service, full GitHub App, full GitLab App, or new language ecosystem support.

## Architecture Impact

The existing pipeline stays intact:

- discovery
- mining
- synthesis
- diff analysis
- canary
- reporters
- CLI

Stable release adds a release rail around it:

- artifact validation
- friendly CLI errors
- package metadata and build gates
- quality tooling
- release docs and checklist

## Risks

- Over-claiming sandboxing would be dangerous. v1 local release documents external sandboxing instead.
- Adding too many new features before release gates would make stability harder to prove.
- Live ecosystem API checks can be flaky and should not be required for automated release tests.

## Verification Strategy

Use fixture-first tests for deterministic product behavior. Use build, ruff, mypy, and CLI smoke commands as release gates. Do not mark stable complete until all gates pass.
