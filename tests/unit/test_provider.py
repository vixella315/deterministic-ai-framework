import pytest
from deterministic.providers import AIProvider, ProviderRequest, ProviderResponse

class FakeProvider(AIProvider):
    name = "fake"
    def generate(self, request):
        return ProviderResponse(
            raw_output='{"content": {}}',
            provider=self.name,
            model="fake-model",
            request_id="req-1",
        )

def test_provider_contract_returns_untrusted_raw_output():
    response = FakeProvider().generate(ProviderRequest(prompt="test"))
    assert response.raw_output == '{"content": {}}'
    assert response.provider == "fake"
    assert response.model == "fake-model"

def test_provider_interface_requires_generate():
    assert getattr(AIProvider.generate, "__isabstractmethod__", False)

def test_provider_response_preserves_request_identity():
    response = FakeProvider().generate(ProviderRequest(prompt="test"))
    assert response.request_id == "req-1"
