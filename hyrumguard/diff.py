from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DiffFacts:
    files: list[str] = field(default_factory=list)
    added_lines: list[str] = field(default_factory=list)
    removed_lines: list[str] = field(default_factory=list)
    changed_subjects: set[str] = field(default_factory=set)
    raw: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "files": self.files,
            "added_lines": self.added_lines,
            "removed_lines": self.removed_lines,
            "changed_subjects": sorted(self.changed_subjects),
        }


def parse_unified_diff(text: str) -> DiffFacts:
    facts = DiffFacts(raw=text)
    current_file: str | None = None
    for line in text.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4:
                current_file = parts[3][2:] if parts[3].startswith("b/") else parts[3]
                if current_file not in facts.files:
                    facts.files.append(current_file)
                _add_path_subjects(facts.changed_subjects, current_file)
            continue
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            continue
        if line.startswith("+"):
            payload = line[1:]
            facts.added_lines.append(payload)
            _add_line_subjects(facts.changed_subjects, payload)
        elif line.startswith("-"):
            payload = line[1:]
            facts.removed_lines.append(payload)
            _add_line_subjects(facts.changed_subjects, payload)
    facts.files.sort()
    return facts


def git_diff(base: str | None = None, head: str | None = None, cwd: str | Path = ".") -> DiffFacts:
    args = ["git", "diff"]
    if base and head:
        args.append(f"{base}...{head}")
    elif base:
        args.append(base)
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    return parse_unified_diff(result.stdout)


def _add_path_subjects(subjects: set[str], path: str) -> None:
    for part in re.split(r"[/._-]+", path):
        if part:
            subjects.add(part)
    stem = Path(path).stem
    if stem:
        subjects.add(stem)


def _add_line_subjects(subjects: set[str], line: str) -> None:
    for pattern in [
        r"""["']([^"']+)["']""",
        r"\bdef\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"\bfunction\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"\b([A-Za-z_][A-Za-z0-9_]*)\s*[:=]",
    ]:
        for match in re.finditer(pattern, line):
            value = match.group(1)
            if value:
                subjects.add(value)
    for match in re.finditer(r"\.([A-Za-z_][A-Za-z0-9_]*)", line):
        subjects.add(match.group(1))
