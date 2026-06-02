from __future__ import annotations

from pathlib import Path

from hyrumguard.models import ContractAtom

from .javascript import mine_javascript_file
from .python import mine_python_file


PYTHON_EXTENSIONS = {".py"}
JAVASCRIPT_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", ".pytest_cache"}


def mine_repository(path: str | Path, target_package: str, dependent: str | None = None) -> list[ContractAtom]:
    repo = Path(path)
    if not repo.exists():
        raise FileNotFoundError(f"Dependent repository not found: {repo}")
    dependent_name = dependent or repo.name
    atoms: list[ContractAtom] = []
    for file_path in sorted(_iter_source_files(repo)):
        relative = file_path.relative_to(repo).as_posix()
        if file_path.suffix in PYTHON_EXTENSIONS:
            atoms.extend(mine_python_file(file_path, relative, target_package, dependent_name))
        elif file_path.suffix in JAVASCRIPT_EXTENSIONS:
            atoms.extend(mine_javascript_file(file_path, relative, target_package, dependent_name))
    return _dedupe_atoms(atoms)


def _iter_source_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix in PYTHON_EXTENSIONS | JAVASCRIPT_EXTENSIONS:
            yield path


def _dedupe_atoms(atoms: list[ContractAtom]) -> list[ContractAtom]:
    seen: set[tuple[str, str, str, str, int]] = set()
    unique: list[ContractAtom] = []
    for atom in atoms:
        key = (atom.type, atom.target_package, atom.subject, atom.evidence.path, atom.evidence.line)
        if key in seen:
            continue
        seen.add(key)
        unique.append(atom)
    return sorted(unique, key=lambda atom: (atom.type, atom.subject, atom.evidence.path, atom.evidence.line))
