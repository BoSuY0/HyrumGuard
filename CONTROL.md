# HyrumGuard Continuous Hardening Control Surface

## Current Mode

- Mode: continuous improvement after public `v1.0.0`
- Public repository: `BoSuY0/HyrumGuard`
- Public release: `v1.0.0`
- User stop rule: continue until the user explicitly ends the work
- Commit rule: commit after each completed task or TODO
- Verification rule: no completion claim without fresh command evidence

## Current Batch

- CB-0: durable goal/spec/plan/control state
- CB-1: risk suppression policy
- CB-2: first-run init command
- CB-3: docs and architecture notes
- CB-4: full local regression gates

## Safety Boundaries

- Canary execution default: dry-run
- Real downstream execution: explicit `--execute --allow-unsafe-execution` only
- Suppressions must remain auditable and must not silently delete findings
- Generated runtime outputs stay out of git

## Pivot Gates

Require explicit new user approval before:

- publishing to PyPI/TestPyPI
- adding hosted services or app backends
- adding language ecosystems beyond Python and JavaScript/TypeScript
- rewriting public release history
- making canary execution blocking by default

## Known External Caveat

Public GitHub Actions jobs are blocked before startup by an account billing lock. Local gates are the authoritative engineering signal until that external account state is fixed.
