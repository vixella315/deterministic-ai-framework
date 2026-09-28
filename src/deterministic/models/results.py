"""Canonical validation result model."""

from dataclasses import dataclass, field
from enum import Enum

from .errors import ErrorDetail


class ValidationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of validating an asset against a contract."""

    status: ValidationStatus
    schema_version: str
    validator_version: str
    errors: tuple[ErrorDetail, ...] = field(default_factory=tuple)
    warnings: tuple[ErrorDetail, ...] = field(default_factory=tuple)

    @property
    def is_valid(self) -> bool:
        return self.status is ValidationStatus.PASS

    @property
    def repairable_errors(self) -> tuple[ErrorDetail, ...]:
        return tuple(error for error in self.errors if error.repairable)

    @property
    def fatal_errors(self) -> tuple[ErrorDetail, ...]:
        return tuple(
            error
            for error in self.errors
            if error.severity == "fatal" or not error.repairable
        )
