from dataclasses import dataclass, field
from typing import Any, Dict
import uuid
import time


@dataclass
class Asset:
    """
    Asset Integration Protocol (AIP)

    Every generated asset must conform to this structure.
    This ensures auditability, traceability, and compliance.
    """

    content: Dict[str, Any]
    schema_version: str = "1.0"
    asset_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    compliance_score: float = 0.0
    valid: bool = False

    def mark_valid(self, score: float = 1.0):
        self.valid = True
        self.compliance_score = score

    def mark_invalid(self):
        self.valid = False
        self.compliance_score = 0.0
