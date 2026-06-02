# HyrumGuard v0.1 Design

## Observed Facts

- The repository at `/home/tetra/Documents/HyrumGuard` started empty except for `.git`.
- The research report at `/home/tetra/Downloads/deep-research-report.md` defines HyrumGuard as a maintainer-facing OSS tool for downstream discovery, implicit usage mining, shadow-contract synthesis, PR-time risk analysis, changed-only canary validation, and reports.
- The requested scope is to implement the architecture, plan, structure, and docs from that report.

## Design Decision

Implement v0.1 as a Python CLI package. Python is the smallest practical foundation because it gives a reliable stdlib AST for Python mining, deterministic JSON tooling, subprocess control for optional canary runs, and simple packaging. JavaScript/TypeScript mining starts as robust regex scanning rather than a full parser, because the report's first slice needs explainable contract atoms more than perfect language coverage.

## Architecture

The CLI is split into layers:

- `discovery`: resolves manual seeds and optional ecosyste.ms dependent packages.
- `miners`: scans Python and JS/TS downstream repositories for contract atoms.
- `synthesis`: clusters atoms into a lockfile.
- `diff`: extracts changed files, symbols, private names, error text, and JSON keys from git or explicit diffs.
- `analysis`: maps diff facts to shadow contracts and produces risk clusters.
- `canary`: selects affected downstreams and optionally executes explicit commands with timeout/temp-directory isolation.
- `reporters`: emits JSON, Markdown, and SARIF.
- `cli`: wires the flow into `discover`, `infer`, `check`, `canary`, and `report`.

## Data And State

State is file-based:

- `.hyrum/dependents.json`
- `.hyrum/shadow-contracts.lock.json`
- `.hyrum/risks.json`
- `hyrumguard.sarif`
- Markdown report/comment output

Each contract atom records type, target package, subject, dependent repo, path, line, snippet, language, confidence, and metadata.

## Failures And Edges

- Live discovery can fail due to network, rate limits, or API shape changes. Manual seeds remain first-class and tests avoid live network.
- Miners may produce false positives; each finding carries evidence and confidence.
- Downstream tests can be unsafe or flaky. Canary is dry-run by default and requires explicit execution.
- SARIF output must remain valid even when no risks are found.

## Test Strategy

- RED tests first against Python and JS/TS fixture downstreams.
- Fixture-based end-to-end CLI tests with no network.
- Reporter tests assert all formats derive from the same risk model.
- CLI smoke checks verify command availability.

## Rollout

The repo ships as an analysis-first v0.1. Blocking PR gates and hosted integrations are documented as future work, not implied by the local CLI.
