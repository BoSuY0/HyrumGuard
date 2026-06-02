from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any

from hyrumguard.models import ContractAtom, stable_id


def synthesize_contracts(atoms: list[ContractAtom], confidence_threshold: float = 0.7) -> dict[str, Any]:
    grouped: dict[tuple[str, str, str], list[ContractAtom]] = defaultdict(list)
    for atom in atoms:
        if atom.confidence >= confidence_threshold:
            grouped[(atom.type, atom.target_package, atom.subject)].append(atom)

    contracts: list[dict[str, Any]] = []
    for (contract_type, target_package, subject), group in grouped.items():
        downstreams = sorted({atom.evidence.dependent for atom in group})
        confidence = mean(atom.confidence for atom in group)
        contracts.append(
            {
                "id": stable_id("contract", contract_type, target_package, subject),
                "type": contract_type,
                "target_package": target_package,
                "subject": subject,
                "confidence": round(confidence, 3),
                "downstream_count": len(downstreams),
                "downstreams": downstreams,
                "atoms": [atom.to_dict() for atom in sorted(group, key=lambda item: item.id)],
                "evidence": [atom.evidence.to_dict() for atom in sorted(group, key=lambda item: item.id)[:5]],
            }
        )

    return {
        "schema_version": 1,
        "tool": "hyrumguard",
        "contracts": sorted(contracts, key=lambda item: item["id"]),
    }
