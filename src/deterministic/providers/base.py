"""Provider boundary. Providers return untrusted raw model output."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True)
class ProviderRequest:
    prompt: str
    metadata: Mapping[str, Any] | None = None

@dataclass(frozen=True)
class ProviderResponse:
    raw_output: str
    provider: str
    model: str
    request_id: str | None = None
    metadata: Mapping[str, Any] | None = None

class ProviderError(RuntimeError):
    """Raised when a provider cannot return a usable response."""

class AIProvider(ABC):
    """Minimal interface implemented by any model provider."""
    name: str = "unknown"
    version: str = "0.1.0"

    @abstractmethod
    def generate(self, request: ProviderRequest) -> ProviderResponse:
        """Generate raw output. The framework must treat it as untrusted."""
        raise NotImplementedError
