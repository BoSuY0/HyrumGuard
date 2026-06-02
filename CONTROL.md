# HyrumGuard Public Release Control Surface

## Scope

- Public repository: `BoSuY0/HyrumGuard`
- Release tag: `v1.0.0`
- Release channel: public GitHub repository and GitHub Release assets
- PyPI/TestPyPI: optional only when credentials or trusted-publisher configuration are actually available

## Safety

- Canary execution default: dry-run
- Real downstream execution: explicit `--execute --allow-unsafe-execution` only
- External sandboxing remains required for untrusted downstream execution

## Public Release Gates

Required:

- pytest
- ruff
- mypy
- build
- twine check
- CLI help smoke
- fixture smoke flow
- public GitHub repo verification
- public GitHub release verification
- release asset verification

## Pivot Gates

Require explicit new user approval before:

- Publishing to PyPI/TestPyPI if credentials appear but the exact target is ambiguous.
- Adding hosted services or app backends.
- Adding more languages/ecosystems.
- Making canary execution blocking by default.
