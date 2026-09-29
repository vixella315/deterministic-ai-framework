"""JSON Schema validation with structured, stable error results."""

from collections.abc import Mapping
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from deterministic.models import ErrorDetail, ValidationResult, ValidationStatus


class Validator:
    """Validate data against a JSON Schema contract."""

    version = "0.1.0"

    def validate(
        self,
        data: Mapping[str, Any],
        schema: Mapping[str, Any],
    ) -> ValidationResult:
        if not isinstance(data, Mapping):
            error = ErrorDetail(
                code="TYPE_ERROR",
                path="$",
                message="Expected a JSON object.",
                severity="fatal",
                repairable=False,
            )
            return ValidationResult(
                ValidationStatus.FAIL,
                str(schema.get("$id", "unknown")),
                self.version,
                errors=(error,),
            )

        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = tuple(self._to_error(error) for error in validator.iter_errors(data))

        status = ValidationStatus.PASS if not errors else ValidationStatus.FAIL
        return ValidationResult(
            status=status,
            schema_version=str(schema.get("$id", "unknown")),
            validator_version=self.version,
            errors=errors,
        )

    @staticmethod
    def _to_error(error: Any) -> ErrorDetail:
        path = "$"
        for part in error.absolute_path:
            path += f"[{part!r}]" if isinstance(part, int) else f".{part}"

        code = {
            "required": "REQUIRED_FIELD_MISSING",
            "type": "TYPE_ERROR",
            "format": "INVALID_FORMAT",
            "additionalProperties": "UNEXPECTED_PROPERTY",
            "const": "VALUE_OUT_OF_RANGE",
        }.get(error.validator, "SCHEMA_ERROR")

        # jsonschema reports additionalProperties at the parent path.
        # Surface the unexpected property name so a deterministic repair can
        # remove exactly that property without guessing.
        if code == "UNEXPECTED_PROPERTY":
            unexpected = getattr(error, "message", "")
            marker = "' was unexpected"
            if unexpected.startswith("'") and marker in unexpected:
                marker_index = unexpected.rfind(marker)
                property_name = unexpected[1:marker_index]
                if property_name:
                    path = f"{path}.{property_name}"

        repairable = code == "UNEXPECTED_PROPERTY"

        return ErrorDetail(
            code=code,
            path=path,
            message=error.message,
            severity="error",
            repairable=repairable,
            rule_id=str(error.validator),
        )
