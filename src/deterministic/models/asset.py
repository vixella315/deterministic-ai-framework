"""Canonical asset model.

An Asset is the framework's normalized representation of data moving through
the controlled pipeline. It does not claim that the contained data is true.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass
class Asset:
    """A versioned, traceable unit of framework data."""

    content: dict[str, Any]
    schema_version: str
    asset_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        if not isinstance(self.content, dict):
            raise TypeError("content must be a dictionary")
        if not self.schema_version:
            raise ValueError("schema_version must not be empty")
        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")
