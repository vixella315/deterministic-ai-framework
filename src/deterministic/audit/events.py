"""Structured, append-only audit events with redacted payloads."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Mapping
from uuid import uuid4


def _hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    run_id: str
    timestamp: str
    operation: str
    status: str
    framework_version: str = "0.1.0"
    schema_version: str | None = None
    provider: str | None = None
    model: str | None = None
    failure_codes: tuple[str, ...] = ()
    repair_actions: tuple[str, ...] = ()
    reason: str | None = None
    input_hash: str | None = None
    output_hash: str | None = None

    @classmethod
    def create(cls, run_id: str, operation: str, status: str, **kwargs: Any) -> "AuditEvent":
        return cls(
            event_id=str(uuid4()),
            run_id=run_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            operation=operation,
            status=status,
            **kwargs,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AuditTrail:
    """In-memory append-only audit trail; durable storage is a later concern."""

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> AuditEvent:
        self._events.append(event)
        return event

    def events_for_run(self, run_id: str) -> tuple[AuditEvent, ...]:
        return tuple(event for event in self._events if event.run_id == run_id)

    def snapshot(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)

    @staticmethod
    def content_hash(value: Any) -> str:
        return _hash(value)
