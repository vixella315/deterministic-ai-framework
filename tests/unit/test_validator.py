from deterministic.models import ValidationStatus
from deterministic.schema import load_asset_schema
from deterministic.validation import Validator


def valid_asset():
    return {
        "content": {"name": "example"},
        "schema_version": "1.0",
        "asset_id": "550e8400-e29b-41d4-a716-446655440000",
        "created_at": "2026-09-28T18:00:00Z",
    }


def test_valid_asset_passes():
    result = Validator().validate(valid_asset(), load_asset_schema())
    assert result.status is ValidationStatus.PASS
    assert result.errors == ()


def test_missing_required_field_is_structured():
    data = valid_asset()
    del data["asset_id"]
    result = Validator().validate(data, load_asset_schema())
    assert result.status is ValidationStatus.FAIL
    assert result.errors[0].code == "REQUIRED_FIELD_MISSING"


def test_wrong_type_is_structured():
    data = valid_asset()
    data["content"] = "not an object"
    result = Validator().validate(data, load_asset_schema())
    assert result.errors[0].code == "TYPE_ERROR"


def test_invalid_uuid_format_is_structured():
    data = valid_asset()
    data["asset_id"] = "not-a-uuid"
    result = Validator().validate(data, load_asset_schema())
    assert result.errors[0].code == "INVALID_FORMAT"


def test_unexpected_property_is_rejected():
    data = valid_asset()
    data["unexpected"] = True
    result = Validator().validate(data, load_asset_schema())
    assert result.errors[0].code == "UNEXPECTED_PROPERTY"


def test_non_object_input_is_fatal():
    result = Validator().validate([], load_asset_schema())
    assert result.status is ValidationStatus.FAIL
    assert result.errors[0].severity == "fatal"


def test_multiple_errors_are_reported_together():
    data = valid_asset()
    del data["asset_id"]
    data["content"] = "wrong"
    result = Validator().validate(data, load_asset_schema())
    assert len(result.errors) >= 2
