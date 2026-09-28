"""Fail-closed stop controller."""

from dataclasses import dataclass
from enum import Enum

from deterministic.validation.failures import FailureAction, get_failure_rule


class StopState(str, Enum):
    ACCEPTED = "ACCEPTED"
    REPAIRED_AND_ACCEPTED = "REPAIRED_AND_ACCEPTED"
    REJECTED = "REJECTED"
    STOPPED = "STOPPED"
    PROVIDER_FAILURE = "PROVIDER_FAILURE"
    SYSTEM_FAILURE = "SYSTEM_FAILURE"


@dataclass(frozen=True)
class StopDecision:
    state: StopState
    reason: str


class StopController:
    """Convert failure outcomes into explicit terminal decisions."""

    version = "0.1.0"

    def decide(self, failures: list[dict] | tuple[dict, ...]) -> StopDecision:
        if not failures:
            return StopDecision(StopState.ACCEPTED, "No failures reported.")

        for failure in failures:
            code = failure.get("code", "SYSTEM_ERROR")
            rule = get_failure_rule(code)

            if rule.action is FailureAction.STOP:
                if code in {"PROVIDER_ERROR", "PROVIDER_TIMEOUT", "PROVIDER_UNAVAILABLE"}:
                    state = StopState.PROVIDER_FAILURE
                elif code == "SYSTEM_ERROR":
                    state = StopState.SYSTEM_FAILURE
                else:
                    state = StopState.STOPPED
                return StopDecision(state, f"{code}: {rule.reason}")

        return StopDecision(
            StopState.REJECTED,
            "Failures remain but no acceptance decision is authorized until repair and revalidation.",
        )

    def accept_repaired(self, revalidation_passed: bool) -> StopDecision:
        if revalidation_passed:
            return StopDecision(
                StopState.REPAIRED_AND_ACCEPTED,
                "Repair completed and revalidation passed.",
            )
        return StopDecision(
            StopState.STOPPED,
            "Repair cannot be accepted because revalidation did not pass.",
        )
