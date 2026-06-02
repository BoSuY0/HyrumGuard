# Notes

## 2026-06-02

- Research report defines the MVP as npm/PyPI, JavaScript/TypeScript and Python, four contract atom types, PR diff matching, optional changed-only canary validation, and JSON/Markdown/SARIF output.
- ecosyste.ms API docs state the common base URL pattern as `https://{service}.ecosyste.ms/api/v1`; search results also confirm a package dependent endpoint shaped like `/registries/{registryName}/packages/{packageName}/dependent_packages`.
- GitHub dependents scraping is intentionally not implemented in v0.1; manual seeds and ecosyste.ms are enough for the report's first slice.
- Stable release scope is local CLI/package release candidate, not hosted service parity.
- Canary execution now requires both `--execute` and `--allow-unsafe-execution`; timeout is reported as a canary result instead of escaping as an exception.
- Public release scope is GitHub-public source plus GitHub Release `v1.0.0` with wheel/sdist assets.
- PyPI publication is not claimed because no PyPI/TestPyPI credentials or trusted-publisher proof are present.
- The first tag-triggered release workflow failed before steps/logs were available; manual `gh release create` was used to complete the public release with the same verified local assets.
- GitHub Actions is enabled for the repo, but job startup is blocked by an account billing lock; public CI will remain red until that external account issue is resolved.
- Current hardening loop should keep the public release as historical baseline and open small verified batches. The user explicitly controls when the loop ends.
- Suppressed risks stay in the risk artifact for auditability. Active risk counts use `summary.risk_count`; full matched counts use `summary.total_risk_count`.
- Starter config lives in `hyrumguard.config.STARTER_CONFIG` so CLI initialization and tests share one canonical example.
