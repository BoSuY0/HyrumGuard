# Contract Atoms

Contract atoms are small pieces of downstream evidence. Synthesis groups them into shadow contracts.

## `symbol_use`

A downstream imports or references a public symbol from the target package.

Examples:

- `from demo_lib import parse_result`
- `import { parseResult } from "demo-lib"`

## `private_symbol_use`

A downstream references a private or semi-private path.

Examples:

- `from demo_lib._compat import normalize_payload`
- `require("demo-lib/lib/_secret")`

These are high-severity because maintainers often change private paths without realizing they became observable.

## `error_regex`

A downstream test expects error text or a regex.

Examples:

- `pytest.raises(ValueError, match="missing token")`
- `expect(() => parseResult({})).toThrow(/missing token/)`

## `json_shape_expectation`

A downstream test or code path expects a JSON key.

Examples:

- `payload["status"]`
- `expect(payload).toHaveProperty("status")`

## Evidence

Each atom includes:

- dependent name
- relative path
- line number
- source snippet
- language
- confidence

This makes every report auditable rather than model-only.
