from __future__ import annotations

import json
from typing import Any


def render_json(risks: dict[str, Any]) -> str:
    return json.dumps(risks, indent=2, sort_keys=True) + "\n"
