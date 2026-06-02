# Integrations

## GitHub Actions

The repository includes a composite action in `action.yml`. A consumer workflow can run HyrumGuard and upload SARIF:

```yaml
name: hyrumguard
on:
  pull_request:
  workflow_dispatch:

jobs:
  guard:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: BoSuY0/HyrumGuard@v1.0.0
        with:
          config: .hyrumguard.yml

      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: hyrumguard.sarif
```

## GitLab

The stable local release supports GitLab as a CLI artifact flow rather than a full app. Run the same commands in CI, store JSON/Markdown artifacts, and use GitLab's MR API or job artifacts to surface the Markdown report.

## PR Comments

Markdown output is designed as a PR/MR comment body. Posting the comment is intentionally left to the workflow runner so maintainers can choose `gh`, GitLab API calls, or non-comment artifact publication.

## Validation

CI should validate artifacts before upload or posting:

```bash
python -m hyrumguard.cli validate \
  --dependents .hyrum/dependents.json \
  --contracts .hyrum/shadow-contracts.lock.json \
  --risks .hyrum/risks.json \
  --sarif hyrumguard.sarif
```
