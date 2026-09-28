"""Structured validation error model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorDetail:
    """One machine-readable validation or policy failure."""

    code: str
    path: str
    message: str
    severity: str = "error"
    repairable: bool = False
    rule_id: str | None = None

    def __post_init__(self) -> None:
        if not self.code:
            raise ValueError("code must not be empty")
        if self.severity not in {"warning", "error", "fatal"}:
            raise ValueError("severity must be warning, error, or fatal")
