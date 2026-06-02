from __future__ import annotations

import ast
import re
from pathlib import Path

from hyrumguard.models import ContractAtom, Evidence


STRING_RE = r"""["']([^"']+)["']"""


def mine_python_file(
    file_path: Path,
    relative_path: str,
    target_package: str,
    dependent: str,
) -> list[ContractAtom]:
    text = file_path.read_text(errors="ignore")
    lines = text.splitlines()
    atoms: list[ContractAtom] = []

    try:
        tree = ast.parse(text)
    except SyntaxError:
        tree = None

    if tree is not None:
        atoms.extend(_mine_imports(tree, lines, relative_path, target_package, dependent))
    atoms.extend(_mine_line_patterns(lines, relative_path, target_package, dependent))
    return atoms


def _mine_imports(
    tree: ast.AST,
    lines: list[str],
    relative_path: str,
    target_package: str,
    dependent: str,
) -> list[ContractAtom]:
    atoms: list[ContractAtom] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == target_package or alias.name.startswith(f"{target_package}."):
                    atom_type = "private_symbol_use" if _has_private_segment(alias.name) else "symbol_use"
                    atoms.append(_atom(atom_type, target_package, alias.name, lines, node.lineno, relative_path, dependent, "python", 0.76))
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module == target_package or node.module.startswith(f"{target_package}."):
                for alias in node.names:
                    subject = f"{node.module}.{alias.name}" if node.module != target_package else alias.name
                    atom_type = "private_symbol_use" if _has_private_segment(subject) else "symbol_use"
                    atoms.append(_atom(atom_type, target_package, subject, lines, node.lineno, relative_path, dependent, "python", 0.86))
    return atoms


def _mine_line_patterns(
    lines: list[str],
    relative_path: str,
    target_package: str,
    dependent: str,
) -> list[ContractAtom]:
    atoms: list[ContractAtom] = []
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        for message in _error_regex_subjects(stripped):
            atoms.append(_atom("error_regex", target_package, message, lines, index, relative_path, dependent, "python", 0.82))
        for key in _json_key_subjects(stripped):
            atoms.append(_atom("json_shape_expectation", target_package, key, lines, index, relative_path, dependent, "python", 0.74))
        for subject in _target_attribute_subjects(stripped, target_package):
            atom_type = "private_symbol_use" if _has_private_segment(subject) else "symbol_use"
            atoms.append(_atom(atom_type, target_package, subject, lines, index, relative_path, dependent, "python", 0.72))
    return atoms


def _error_regex_subjects(line: str) -> list[str]:
    subjects: list[str] = []
    for pattern in [
        rf"match\s*=\s*{STRING_RE}",
        rf"re\.search\(\s*{STRING_RE}",
        rf"raises\([^)]*,\s*{STRING_RE}",
    ]:
        subjects.extend(match.group(1) for match in re.finditer(pattern, line))
    return subjects


def _json_key_subjects(line: str) -> list[str]:
    subjects: list[str] = []
    subjects.extend(match.group(1) for match in re.finditer(r"""\[[\"']([A-Za-z_][A-Za-z0-9_-]*)[\"']\]""", line))
    subjects.extend(match.group(1) for match in re.finditer(r"""[\"']([A-Za-z_][A-Za-z0-9_-]*)[\"']\s+in\s+[A-Za-z_][A-Za-z0-9_]*""", line))
    subjects.extend(match.group(1) for match in re.finditer(r"""\.get\(\s*[\"']([A-Za-z_][A-Za-z0-9_-]*)[\"']""", line))
    return subjects


def _target_attribute_subjects(line: str, target_package: str) -> list[str]:
    subjects: list[str] = []
    escaped = re.escape(target_package)
    for match in re.finditer(rf"\b{escaped}\.([A-Za-z_][A-Za-z0-9_\.]*)", line):
        subjects.append(f"{target_package}.{match.group(1).rstrip('(')}")
    return subjects


def _has_private_segment(subject: str) -> bool:
    return any(segment.startswith("_") for segment in subject.split("."))


def _atom(
    atom_type: str,
    target_package: str,
    subject: str,
    lines: list[str],
    line: int,
    relative_path: str,
    dependent: str,
    language: str,
    confidence: float,
) -> ContractAtom:
    snippet = lines[line - 1].strip() if 0 < line <= len(lines) else ""
    return ContractAtom(
        type=atom_type,
        target_package=target_package,
        subject=subject,
        evidence=Evidence(dependent=dependent, path=relative_path, line=line, snippet=snippet),
        language=language,
        confidence=confidence,
    )
