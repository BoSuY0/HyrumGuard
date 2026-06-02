from pathlib import Path

from hyrumguard.miners import mine_repository
from hyrumguard.synthesis import synthesize_contracts


FIXTURES = Path(__file__).parent / "fixtures" / "downstreams"


def test_mines_python_contract_atoms():
    atoms = mine_repository(
        FIXTURES / "python_client",
        target_package="demo_lib",
        dependent="python-client",
    )

    by_type = {atom.type for atom in atoms}
    subjects = {atom.subject for atom in atoms}

    assert {"symbol_use", "private_symbol_use", "error_regex", "json_shape_expectation"} <= by_type
    assert "parse_result" in subjects
    assert "Client" in subjects
    assert "demo_lib._compat.normalize_payload" in subjects
    assert "missing token" in subjects
    assert "status" in subjects
    assert all(atom.evidence.path and atom.evidence.line > 0 for atom in atoms)


def test_mines_javascript_contract_atoms():
    atoms = mine_repository(
        FIXTURES / "js_client",
        target_package="demo-lib",
        dependent="js-client",
    )

    by_type = {atom.type for atom in atoms}
    subjects = {atom.subject for atom in atoms}

    assert {"symbol_use", "private_symbol_use", "error_regex", "json_shape_expectation"} <= by_type
    assert "parseResult" in subjects
    assert "Client" in subjects
    assert "demo-lib/lib/_secret" in subjects
    assert "missing token" in subjects
    assert "status" in subjects


def test_synthesizes_deterministic_shadow_contracts():
    atoms = []
    atoms.extend(mine_repository(FIXTURES / "python_client", "demo_lib", "python-client"))
    atoms.extend(mine_repository(FIXTURES / "js_client", "demo-lib", "js-client"))

    lockfile = synthesize_contracts(atoms, confidence_threshold=0.5)
    contracts = lockfile["contracts"]

    assert lockfile["schema_version"] == 1
    assert contracts == sorted(contracts, key=lambda item: item["id"])
    assert any(contract["type"] == "error_regex" and contract["subject"] == "missing token" for contract in contracts)
    assert all(contract["downstream_count"] >= 1 for contract in contracts)
