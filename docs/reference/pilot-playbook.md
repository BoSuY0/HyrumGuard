# Pilot Playbook

Use HyrumGuard first as a non-blocking reviewer.

## Pick Pilot Repositories

Choose 3-5 libraries with:

- visible public dependents
- frequent PRs
- error-heavy, event-heavy, or JSON-heavy APIs
- maintainers willing to label findings as useful or noisy

## Run Non-Blocking

1. Commit or generate `.hyrum/dependents.json`.
2. Run `infer` to create a lockfile.
3. Run `check` on PRs.
4. Publish Markdown and SARIF.
5. Track whether maintainers changed PRs because of alerts.

## Success Metrics

- Precision: at least two thirds of alerts are judged useful.
- Prevention value: at least 2-3 PRs are changed before merge during pilots.
- Runtime: affected-only checks remain short enough for normal PR feedback.
- Coverage utility: each pilot gets at least one meaningful contract atom from real downstream code.

If precision is low, narrow the domain before adding more contract types.
