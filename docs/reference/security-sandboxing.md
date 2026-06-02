# Security And Sandboxing

Downstream repositories are untrusted code. HyrumGuard therefore separates analysis from execution.

## Defaults

- Mining is static.
- Canary mode is dry-run unless `--execute --allow-unsafe-execution` is passed.
- Live discovery is optional.
- Tests in this repository do not call live ecosystem APIs.

## Canary Execution

When `--execute --allow-unsafe-execution` is used, HyrumGuard:

- selects only configured dependents
- copies each dependent into a temporary directory
- runs the configured command with a timeout
- stores stdout/stderr tails in the canary result

The stable local release does not enforce network isolation. For unknown downstreams, run HyrumGuard inside a container, VM, CI sandbox, or dedicated ephemeral runner with network disabled.

## Suppression And Blocking

Blocking mode is a workflow decision. HyrumGuard reports risk; maintainers decide whether a risk should block merge.
