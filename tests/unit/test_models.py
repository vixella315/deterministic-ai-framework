from datetime import datetime, timezone
from uuid import UUID

import pytest

from deterministic.models import Asset, ErrorDetail, ValidationResult, ValidationStatus


def test_asset_has_traceable_identity_and_utc_timestamp():
    asset = Asset({"name": "example"}, "1.0")
    assert isinstance(asset.asset_id, UUID)
    assert asset.created_at.tzinfo == timezone.utc
    assert asset.schema_version == "1.0"


def test_asset_rejects_non_mapping_content():
    with pytest.raises(TypeError):
        Asset(["not", "an", "object"], "1.0")


def test_asset_requires_schema_version():
    with pytest.raises(ValueError):
        Asset({}, "")


def test_asset_rejects_naive_timestamp():
    with pytest.raises(ValueError):
        Asset({}, "1.0", created_at=datetime(2026, 1, 1))


def test_error_detail_is_structured_and_immutable():
    error = ErrorDetail("TYPE_ERROR", "$.age", "Expected integer", repairable=True)
    assert error.repairable is True
    assert error.path == "$.age"
    with pytest.raises(Exception):
        error.code = "OTHER"


def test_validation_result_separates_repairable_and_fatal_errors():
    repairable = ErrorDetail("EMPTY_VALUE", "$.name", "Empty", repairable=True)
    fatal = ErrorDetail("SECURITY_VIOLATION", "$", "Blocked", severity="fatal")
    result = ValidationResult(
        ValidationStatus.FAIL,
        "1.0",
        "0.1.0",
        errors=(repairable, fatal),
    )
    assert not result.is_valid
    assert result.repairable_errors == (repairable,)
    assert result.fatal_errors == (fatal,)
