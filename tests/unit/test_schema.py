from deterministic.schema import load_asset_schema

def test_asset_schema_has_canonical_draft_and_required_fields():
    schema = load_asset_schema()
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["required"] == ["content", "schema_version", "asset_id", "created_at"]
    assert schema["additionalProperties"] is False

def test_asset_schema_loader_returns_independent_data():
    first = load_asset_schema()
    second = load_asset_schema()
    first["title"] = "changed"
    assert second["title"] != "changed"

def test_asset_schema_defines_explicit_version_contract():
    schema = load_asset_schema()
    assert schema["properties"]["schema_version"]["const"] == "1.0"
