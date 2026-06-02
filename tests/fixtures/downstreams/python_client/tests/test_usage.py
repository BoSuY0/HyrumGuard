import re

import pytest
import demo_lib
from demo_lib import Client, parse_result
from demo_lib._compat import normalize_payload


def test_error_message_contract():
    with pytest.raises(ValueError, match="missing token"):
        parse_result({})


def test_json_shape_contract():
    payload = Client().to_json()
    assert payload["status"] == "ok"
    assert "items" in payload


def test_private_symbol_contract():
    assert normalize_payload({"status": "ok"})["status"] == "ok"
    assert re.search("missing token", "missing token")
