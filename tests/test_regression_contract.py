import json
from deterministic.orchestration import Orchestrator,StopState
from deterministic.providers import AIProvider,ProviderResponse
class Provider(AIProvider):
    name="regression"
    def __init__(self,output): self.output=output
    def generate(self,request): return ProviderResponse(self.output,self.name,"test")
SCHEMA={"type":"object","properties":{"name":{"type":"string","minLength":1},"age":{"type":"integer","minimum":0}},"required":["name"],"additionalProperties":False}
def test_accepted_output_is_unchanged():
    output={"name":"Ada","age":36}; r=Orchestrator(Provider(json.dumps(output))).run("test",SCHEMA); assert r.state is StopState.ACCEPTED and r.output==output
def test_repair_never_creates_required_values():
    r=Orchestrator(Provider('{"age":36}')).run("test",SCHEMA); assert r.state is StopState.STOPPED and r.output is None
def test_invalid_semantic_value_does_not_get_guessed():
    r=Orchestrator(Provider('{"name":"","age":36}')).run("test",SCHEMA); assert r.state is StopState.STOPPED and r.output is None
