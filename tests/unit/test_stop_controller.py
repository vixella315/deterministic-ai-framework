from deterministic.orchestration import StopController, StopState


def test_no_failures_accepts():
    assert StopController().decide([]).state is StopState.ACCEPTED


def test_security_failure_stops():
    decision = StopController().decide([{"code": "SECURITY_VIOLATION"}])
    assert decision.state is StopState.STOPPED


def test_provider_failure_has_distinct_terminal_state():
    decision = StopController().decide([{"code": "PROVIDER_TIMEOUT"}])
    assert decision.state is StopState.PROVIDER_FAILURE


def test_system_failure_has_distinct_terminal_state():
    decision = StopController().decide([{"code": "SYSTEM_ERROR"}])
    assert decision.state is StopState.SYSTEM_FAILURE


def test_repairable_failure_cannot_be_accepted_without_revalidation():
    decision = StopController().decide([{"code": "REQUIRED_FIELD_MISSING"}])
    assert decision.state is StopState.REJECTED


def test_repaired_output_requires_revalidation():
    controller = StopController()
    assert controller.accept_repaired(False).state is StopState.STOPPED
    assert controller.accept_repaired(True).state is StopState.REPAIRED_AND_ACCEPTED
