from deterministic.validation.failures import FailureCode,get_failure_rule
def test_every_failure_code_has_a_rule():
    for code in FailureCode:
        rule=get_failure_rule(code.value); assert rule.code==code.value and rule.action is not None and rule.reason
def test_security_and_provider_failures_are_not_repairable():
    for code in (FailureCode.SECURITY_VIOLATION,FailureCode.PROVIDER_ERROR,FailureCode.PROVIDER_TIMEOUT,FailureCode.PROVIDER_UNAVAILABLE): assert not get_failure_rule(code.value).default_repairable
def test_only_current_repairable_failure_is_unexpected_property(): assert [c.value for c in FailureCode if get_failure_rule(c.value).default_repairable]==[FailureCode.UNEXPECTED_PROPERTY.value]
