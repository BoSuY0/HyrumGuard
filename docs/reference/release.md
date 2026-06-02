# Release Process

HyrumGuard's stable public release channel is GitHub:

- Repository: `https://github.com/BoSuY0/HyrumGuard`
- Release: `v1.0.0`
- Assets: `hyrumguard-1.0.0.tar.gz` and `hyrumguard-1.0.0-py3-none-any.whl`

## Required Gates

Run from the repository root:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m ruff check .
.venv/bin/python -m mypy hyrumguard
rm -rf dist build hyrumguard.egg-info
.venv/bin/python -m build
.venv/bin/python -m twine check dist/*
```

## Fixture Smoke Flow

```bash
tmpdir=$(mktemp -d)
.venv/bin/python -m hyrumguard.cli discover demo_lib --config .hyrumguard.yml --out "$tmpdir/dependents.json"
.venv/bin/python -m hyrumguard.cli infer --from "$tmpdir/dependents.json" --out "$tmpdir/shadow-contracts.lock.json"
.venv/bin/python -m hyrumguard.cli check --contracts "$tmpdir/shadow-contracts.lock.json" --diff-file tests/fixtures/sample.diff --out "$tmpdir/risks.json"
.venv/bin/python -m hyrumguard.cli report --risks "$tmpdir/risks.json" --format markdown --out "$tmpdir/report.md"
.venv/bin/python -m hyrumguard.cli report --risks "$tmpdir/risks.json" --format sarif --out "$tmpdir/hyrumguard.sarif"
.venv/bin/python -m hyrumguard.cli validate --dependents "$tmpdir/dependents.json" --contracts "$tmpdir/shadow-contracts.lock.json" --risks "$tmpdir/risks.json" --sarif "$tmpdir/hyrumguard.sarif"
.venv/bin/python -m hyrumguard.cli canary --risks "$tmpdir/risks.json" --dependents "$tmpdir/dependents.json" --affected-only --out "$tmpdir/canary.json"
rm -rf "$tmpdir"
```

Expected high-level output:

- discover writes 1 fixture dependent
- infer writes 8 fixture shadow contracts
- check writes 5 fixture risks
- validate accepts 4 artifacts
- canary writes a dry-run plan for 1 dependent

## Publish Boundary

Do not claim PyPI publication unless a real PyPI/TestPyPI upload succeeds and is verified. GitHub Release publication is the public release channel for `v1.0.0`.

## Public Verification

```bash
gh repo view BoSuY0/HyrumGuard --json nameWithOwner,visibility,url
gh release view v1.0.0 --repo BoSuY0/HyrumGuard --json tagName,url,isDraft,isPrerelease
gh release view v1.0.0 --repo BoSuY0/HyrumGuard --json assets
```
