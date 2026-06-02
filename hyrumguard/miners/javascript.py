from __future__ import annotations

import re
from pathlib import Path

from hyrumguard.models import ContractAtom, Evidence


def mine_javascript_file(
    file_path: Path,
    relative_path: str,
    target_package: str,
    dependent: str,
) -> list[ContractAtom]:
    lines = file_path.read_text(errors="ignore").splitlines()
    atoms: list[ContractAtom] = []
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        atoms.extend(_mine_imports(stripped, lines, index, relative_path, target_package, dependent))
        atoms.extend(_mine_errors(stripped, lines, index, relative_path, target_package, dependent))
        atoms.extend(_mine_json_shapes(stripped, lines, index, relative_path, target_package, dependent))
    return atoms


def _mine_imports(
    line: str,
    lines: list[str],
    index: int,
    relative_path: str,
    target_package: str,
    dependent: str,
) -> list[ContractAtom]:
    atoms: list[ContractAtom] = []
    escaped = re.escape(target_package)
    for match in re.finditer(rf"""import\s+\{{([^}}]+)\}}\s+from\s+["']{escaped}["']""", line):
        for name in match.group(1).split(","):
            subject = name.strip().split(" as ")[0].strip()
            if subject:
                atoms.append(_atom("symbol_use", target_package, subject, lines, index, relative_path, dependent, 0.82))
    for match in re.finditer(rf"""require\(\s*["']({escaped}[^"']*)["']\s*\)""", line):
        subject = match.group(1)
        atom_type = "private_symbol_use" if "/_" in subject or "._" in subject else "symbol_use"
        atoms.append(_atom(atom_type, target_package, subject, lines, index, relative_path, dependent, 0.82))
    return atoms


def _mine_errors(
    line: str,
    lines: list[str],
    index: int,
    relative_path: str,
    target_package: str,
    dependent: str,
) -> list[ContractAtom]:
    atoms: list[ContractAtom] = []
    for match in re.finditer(r"toThrow\(\s*/([^/]+)/", line):
        atoms.append(_atom("error_regex", target_package, match.group(1), lines, index, relative_path, dependent, 0.8))
    for match in re.finditer(r"""toThrow\(\s*["']([^"']+)["']""", line):
        atoms.append(_atom("error_regex", target_package, match.group(1), lines, index, relative_path, dependent, 0.78))
    return atoms


def _mine_json_shapes(
    line: str,
    lines: list[str],
    index: int,
    relative_path: str,
    target_package: str,
    dependent: str,
) -> list[ContractAtom]:
    atoms: list[ContractAtom] = []
    for match in re.finditer(r"""toHaveProperty\(\s*["']([A-Za-z_][A-Za-z0-9_-]*)["']""", line):
        atoms.append(_atom("json_shape_expectation", target_package, match.group(1), lines, index, relative_path, dependent, 0.76))
    for match in re.finditer(r"""\bpayload\.([A-Za-z_][A-Za-z0-9_]*)""", line):
        atoms.append(_atom("json_shape_expectation", target_package, match.group(1), lines, index, relative_path, dependent, 0.68))
    return atoms


def _atom(
    atom_type: str,
    target_package: str,
    subject: str,
    lines: list[str],
    line: int,
    relative_path: str,
    dependent: str,
    confidence: float,
) -> ContractAtom:
    return ContractAtom(
        type=atom_type,
        target_package=target_package,
        subject=subject,
        evidence=Evidence(dependent=dependent, path=relative_path, line=line, snippet=lines[line - 1].strip()),
        language="javascript",
        confidence=confidence,
    )
