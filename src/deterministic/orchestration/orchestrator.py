"""End-to-end orchestration of the deterministic control pipeline."""

import json
from dataclasses import dataclass
from typing import Any

from deterministic.providers import AIProvider, ProviderRequest, ProviderResponse, ProviderError
from deterministic.repair import RepairEngine
from deterministic.validation import Validator
from deterministic.validation.failures import FailureCode
from deterministic.orchestration.stop_controller import StopController, StopState


@dataclass(frozen=True)
class OrchestrationResult:
    state: StopState
    output: dict[str, Any] | None
    provider_response: ProviderResponse | None
    validation: Any | None
    repair_actions: tuple[str, ...] = ()
    reason: str | None = None


class Orchestrator:
    """Coordinate provider output, validation, repair, revalidation, and stopping."""

    version = "0.1.0"

    def __init__(
        self,
        provider: AIProvider,
        validator: Validator | None = None,
        repair_engine: RepairEngine | None = None,
        stop_controller: StopController | None = None,
    ):
        self.provider = provider
        self.validator = validator or Validator()
        self.repair_engine = repair_engine or RepairEngine()
        self.stop_controller = stop_controller or StopController()

    def run(self, prompt: str, schema: dict[str, Any]) -> OrchestrationResult:
        try:
            response = self.provider.generate(ProviderRequest(prompt=prompt))
        except ProviderError as exc:
            return OrchestrationResult(StopState.PROVIDER_FAILURE, None, None, None, reason=str(exc))
        except Exception as exc:
            return OrchestrationResult(StopState.SYSTEM_FAILURE, None, None, None, reason=str(exc))

        try:
            data = json.loads(response.raw_output)
        except (json.JSONDecodeError, TypeError) as exc:
            return OrchestrationResult(
                StopState.STOPPED,
                None,
                response,
                None,
                reason=f"{FailureCode.PARSE_ERROR.value}: {exc}",
            )

        validation = self.validator.validate(data, schema)
        if validation.valid:
            return OrchestrationResult(
                StopState.ACCEPTED, data, response, validation
            )

        failures = [
            {
                "code": error.code,
                "path": error.path,
                "property": getattr(error, "property", None),
            }
            for error in validation.errors
        ]
        decision = self.stop_controller.decide(failures)
        if decision.state in {
            StopState.STOPPED,
            StopState.PROVIDER_FAILURE,
            StopState.SYSTEM_FAILURE,
        }:
            return OrchestrationResult(
                decision.state, None, response, validation, reason=decision.reason
            )

        repair = self.repair_engine.repair(data, failures)
        if repair.stopped:
            return OrchestrationResult(
                StopState.STOPPED,
                None,
                response,
                validation,
                repair.actions,
                repair.reason,
            )

        revalidation = self.validator.validate(repair.data, schema)
        if not revalidation.valid:
            return OrchestrationResult(
                StopState.STOPPED,
                None,
                response,
                revalidation,
                repair.actions,
                "REVALIDATION_FAILED: repaired output did not satisfy the contract.",
            )

        return OrchestrationResult(
            StopState.REPAIRED_AND_ACCEPTED,
            repair.data,
            response,
            revalidation,
            repair.actions,
            "Repair completed and revalidation passed.",
        )
