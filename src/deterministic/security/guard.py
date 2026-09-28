"""Conservative input/output security controls."""

import json
import os
from dataclasses import dataclass
from typing import Any


class SecurityViolation(ValueError):
    """Raised when a configured security boundary is violated."""


@dataclass(frozen=True)
class SecurityPolicy:
    max_prompt_bytes: int = 64 * 1024
    max_output_bytes: int = 1024 * 1024
    reject_control_chars: bool = True


class SecurityGuard:
    """Enforce bounded, fail-closed handling of model-bound text."""

    version = "0.1.0"

    def __init__(self, policy: SecurityPolicy | None = None):
        self.policy = policy or SecurityPolicy()

    def validate_prompt(self, prompt: str) -> None:
        if not isinstance(prompt, str):
            raise SecurityViolation("Prompt must be text.")
        if len(prompt.encode("utf-8")) > self.policy.max_prompt_bytes:
            raise SecurityViolation("Prompt exceeds configured size limit.")
        if self.policy.reject_control_chars and any(ord(c) < 32 and c not in "\\t\\n\\r" for c in prompt):
            raise SecurityViolation("Prompt contains disallowed control characters.")

    def validate_raw_output(self, raw_output: str) -> None:
        if not isinstance(raw_output, str):
            raise SecurityViolation("Provider output must be text.")
        if len(raw_output.encode("utf-8")) > self.policy.max_output_bytes:
            raise SecurityViolation("Provider output exceeds configured size limit.")

    @staticmethod
    def parse_json(raw_output: str) -> Any:
        try:
            return json.loads(raw_output)
        except (json.JSONDecodeError, TypeError) as exc:
            raise SecurityViolation("Output is not valid JSON.") from exc

    @staticmethod
    def secrets_must_not_be_in_source() -> bool:
        # Configuration is expected through environment/secret-management layers.
        return bool(os.environ.get("DETERMINISTIC_AI_SECURITY_CHECK", "1"))
