import pytest
from deterministic.validation.failures import FAILURE_RULES, FailureAction, FailureCode, get_failure_rule

def test_taxonomy_is_complete():
    assert set(FAILURE_RULES) == set(FailureCode)

@pytest.mark.parametrize("code",[FailureCode.SECURITY_VIOLATION,FailureCode.POLICY_VIOLATION,FailureCode.UNTRUSTED_CONTENT,FailureCode.REPAIR_FAILED,FailureCode.REVALIDATION_FAILED,FailureCode.SYSTEM_ERROR])
def test_critical_failures_stop(code):
    assert get_failure_rule(code).action is FailureAction.STOP

def test_structural_failures_fail_closed_by_default():
    for code in (FailureCode.REQUIRED_FIELD_MISSING,FailureCode.TYPE_ERROR,FailureCode.INVALID_FORMAT):
        rule=get_failure_rule(code)
        assert rule.action is FailureAction.STOP and not rule.default_repairable

def test_unknown_failure_fails_closed():
    assert get_failure_rule("UNKNOWN").action is FailureAction.STOP

def test_missing_data_never_authorizes_invention():
    assert "never invent" in get_failure_rule(FailureCode.REQUIRED_FIELD_MISSING).reason or get_failure_rule(FailureCode.REQUIRED_FIELD_MISSING).action is FailureAction.STOP
