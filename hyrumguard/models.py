from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha1
from typing import Any


def stable_id(prefix: str, *parts: object) -> str:
    payload = "\0".join(str(part) for part in parts)
    digest = sha1(payload.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


@dataclass(frozen=True)
class Evidence:
    dependent: str
    path: str
    line: int
    snippet: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "dependent": self.dependent,
            "path": self.path,
            "line": self.line,
            "snippet": self.snippet,
        }


@dataclass(frozen=True)
class ContractAtom:
    type: str
    target_package: str
    subject: str
    evidence: Evidence
    language: str
    confidence: float = 0.7
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def id(self) -> str:
        return stable_id(
            "atom",
            self.type,
            self.target_package,
            self.subject,
            self.evidence.dependent,
            self.evidence.path,
            self.evidence.line,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "target_package": self.target_package,
            "subject": self.subject,
            "language": self.language,
            "confidence": round(self.confidence, 3),
            "evidence": self.evidence.to_dict(),
            "metadata": self.metadata,
        }
