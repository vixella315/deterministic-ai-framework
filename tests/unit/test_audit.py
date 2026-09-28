from deterministic.audit import AuditEvent, AuditTrail


def test_event_has_unique_identity_and_run_correlation():
    first = AuditEvent.create("run-1", "request.created", "STARTED")
    second = AuditEvent.create("run-1", "validation.failed", "FAILED")
    assert first.event_id != second.event_id
    assert first.run_id == second.run_id


def test_events_are_retrievable_by_run():
    trail = AuditTrail()
    trail.record(AuditEvent.create("run-1", "request.created", "STARTED"))
    trail.record(AuditEvent.create("run-2", "request.created", "STARTED"))
    assert len(trail.events_for_run("run-1")) == 1


def test_content_hash_is_stable_without_storing_content():
    trail = AuditTrail()
    value={"name":"Ada"}
    assert trail.content_hash(value) == trail.content_hash(value)
    assert "Ada" not in trail.snapshot().__repr__()


def test_failure_and_repair_actions_are_explicit():
    event = AuditEvent.create(
        "run-1",
        "repair.applied",
        "REPAIRED",
        failure_codes=("UNEXPECTED_PROPERTY",),
        repair_actions=("remove:extra",),
    )
    assert event.failure_codes == ("UNEXPECTED_PROPERTY",)
    assert event.repair_actions == ("remove:extra",)
