from deterministic.orchestration import Orchestrator, StopState
from deterministic.providers import AIProvider, ProviderResponse, ProviderError

SCHEMA={"type":"object","properties":{"name":{"type":"string"}},"required":["name"],"additionalProperties":False}
class Provider(AIProvider):
    name="test"
    def __init__(self, output): self.output=output
    def generate(self, request): return ProviderResponse(self.output,self.name,"test-model","r1")

def test_valid_output_is_accepted():
    r=Orchestrator(Provider('{"name":"Ada"}')).run("test",SCHEMA)
    assert r.state is StopState.ACCEPTED and r.output=={"name":"Ada"}
def test_missing_value_stops_without_invention():
    r=Orchestrator(Provider("{}")).run("test",SCHEMA)
    assert r.state is StopState.STOPPED and r.output is None
def test_extra_property_is_removed_then_revalidated():
    r=Orchestrator(Provider('{"name":"Ada","extra":true}')).run("test",SCHEMA)
    assert r.state is StopState.REPAIRED_AND_ACCEPTED and r.output=={"name":"Ada"}
def test_malformed_json_stops():
    assert Orchestrator(Provider("not json")).run("test",SCHEMA).state is StopState.STOPPED
def test_provider_error_stops():
    class Failing(AIProvider):
        def generate(self, request): raise ProviderError("offline")
    assert Orchestrator(Failing()).run("test",SCHEMA).state is StopState.PROVIDER_FAILURE
