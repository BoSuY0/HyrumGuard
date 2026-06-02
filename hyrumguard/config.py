from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    text = config_path.read_text()
    if config_path.suffix.lower() == ".json":
        return json.loads(text)
    return parse_simple_yaml(text)


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse the small YAML subset used by HyrumGuard examples.

    This intentionally supports simple mappings, nested mappings, and lists of
    scalars or one-line mappings. Users with complex YAML can install PyYAML and
    load JSON-equivalent config before passing data to HyrumGuard.
    """
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if line.startswith("- "):
            item_text = line[2:].strip()
            if not isinstance(parent, list):
                raise ValueError(f"List item has no list parent: {raw_line}")
            parent.append(_parse_inline_mapping(item_text) if ":" in item_text else _parse_scalar(item_text))
            continue

        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"Unsupported YAML line: {raw_line}")
        key = key.strip()
        value = value.strip()
        if value:
            parent[key] = _parse_scalar(value)
            continue

        container: dict[str, Any] | list[Any]
        container = [] if _next_non_empty_starts_with_dash(text, raw_line) else {}
        parent[key] = container
        stack.append((indent, container))

    return root


def _next_non_empty_starts_with_dash(text: str, current_line: str) -> bool:
    lines = text.splitlines()
    try:
        start = lines.index(current_line) + 1
    except ValueError:
        return False
    current_indent = len(current_line) - len(current_line.lstrip(" "))
    for line in lines[start:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        return indent > current_indent and line.strip().startswith("- ")
    return False


def _parse_inline_mapping(text: str) -> dict[str, Any]:
    key, _, value = text.partition(":")
    return {key.strip(): _parse_scalar(value.strip())}


def _parse_scalar(value: str) -> Any:
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None", "~"}:
        return None
    if value.startswith(("'", '"')) and value.endswith(("'", '"')):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value
