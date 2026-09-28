"""Load canonical JSON Schema contracts without silently modifying them."""

import json
from pathlib import Path
from typing import Any

_SCHEMA_DIR = Path(__file__).resolve().parent

def load_asset_schema() -> dict[str, Any]:
    """Return a fresh copy of the canonical Asset JSON Schema."""
    path = _SCHEMA_DIR / "asset.schema.json"
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
