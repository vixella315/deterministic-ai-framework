"""Safe, deterministic repairs that never fabricate required information."""

from dataclasses import dataclass
from typing import Any

from deterministic.validation.failures import FailureCode, get_failure_rule


@dataclass(frozen=True)
class RepairResult:
    repaired: bool
    data: dict[str, Any]
    actions: tuple[str, ...] = ()
    stopped: bool = False
    reason: str | None = None


class RepairEngine:
    """Apply only explicitly authorized, lossless structural repairs."""

    version = "0.1.0"

    def repair(
        self,
        data: dict[str, Any],
        failures: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    ) -> RepairResult:
        working = dict(data)
        actions: list[str] = []

        for failure in failures:
            code = failure.get("code")
            rule = get_failure_rule(code)
            if not rule.default_repairable:
                return RepairResult(False, working, tuple(actions), True, f"{code}: repair not permitted")

            # The engine intentionally does not synthesize missing values.
            if code in {FailureCode.REQUIRED_FIELD_MISSING.value, FailureCode.NULL_NOT_ALLOWED.value, FailureCode.EMPTY_VALUE.value}:
                return RepairResult(False, working, tuple(actions), True, f"{code}: no deterministic source supplied")

            if code == FailureCode.UNEXPECTED_PROPERTY.value:
                path = failure.get("path", "")
                property_name = failure.get("property")
                if property_name is None and path.startswith("$"):
                    property_name = path.split(".")[-1] if "." in path else None
                if property_name and property_name in working:
                    del working[property_name]
                    actions.append(f"remove:{property_name}")
                    continue
                return RepairResult(False, working, tuple(actions), True, "UNEXPECTED_PROPERTY: property could not be identified safely")

            return RepairResult(False, working, tuple(actions), True, f"{code}: no safe deterministic repair rule")

        return RepairResult(bool(actions), working, tuple(actions), False, None)
