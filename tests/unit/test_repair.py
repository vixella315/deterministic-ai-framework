from deterministic.repair import RepairEngine


def test_missing_required_value_stops_without_invention():
    data = {"name": "example"}
    result = RepairEngine().repair(
        data, [{"code": "REQUIRED_FIELD_MISSING", "path": "$.asset_id"}]
    )
    assert result.stopped
    assert result.data == data
    assert result.actions == ()


def test_unexpected_property_can_be_removed_explicitly():
    data = {"name": "example", "extra": True}
    result = RepairEngine().repair(
        data, [{"code": "UNEXPECTED_PROPERTY", "path": "$.extra", "property": "extra"}]
    )
    assert not result.stopped
    assert result.repaired
    assert result.data == {"name": "example"}
    assert result.actions == ("remove:extra",)


def test_repair_does_not_mutate_input():
    data = {"name": "example", "extra": True}
    RepairEngine().repair(
        data, [{"code": "UNEXPECTED_PROPERTY", "path": "$.extra", "property": "extra"}]
    )
    assert data == {"name": "example", "extra": True}


def test_unsupported_repair_stops():
    result = RepairEngine().repair(
        {"name": "example"}, [{"code": "INVALID_ENUM", "path": "$.name"}]
    )
    assert result.stopped
