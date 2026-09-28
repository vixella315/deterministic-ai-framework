from deterministic.audit import AuditEvent, AuditTrail
from deterministic.orchestration import Orchestrator, StopState
from deterministic.providers import AIProvider, ProviderResponse, ProviderError
from deterministic.security import SecurityGuard, SecurityViolation
import pytest
SCHEMA={"type":"object","properties":{"name":{"type":"string"}},"required":["name"],"additionalProperties":False}
class StaticProvider(AIProvider):
    name="test-provider"
    def __init__(self,output): self.output=output
    def generate(self,request): return ProviderResponse(self.output,self.name,"test-model","integration-1")
def test_end_to_end_valid_path():
    r=Orchestrator(StaticProvider('{"name":"Ada"}')).run("test",SCHEMA); assert r.state is StopState.ACCEPTED and r.output=={"name":"Ada"}
def test_end_to_end_safe_repair_path():
    r=Orchestrator(StaticProvider('{"name":"Ada","extra":true}')).run("test",SCHEMA); assert r.state is StopState.REPAIRED_AND_ACCEPTED and r.output=={"name":"Ada"}
def test_end_to_end_missing_data_stops():
    r=Orchestrator(StaticProvider("{}")).run("test",SCHEMA); assert r.state is StopState.STOPPED and r.output is None
def test_end_to_end_malformed_output_stops():
    assert Orchestrator(StaticProvider("{broken")).run("test",SCHEMA).state is StopState.STOPPED
def test_end_to_end_provider_failure_is_terminal():
    class Failing(AIProvider):
        def generate(self,request): raise ProviderError("offline")
    assert Orchestrator(Failing()).run("test",SCHEMA).state is StopState.PROVIDER_FAILURE
def test_security_boundary_rejects_oversized_input():
    with pytest.raises(SecurityViolation): SecurityGuard().validate_prompt("x"*(64*1024+1))
def test_audit_reconstructs_event_sequence():
    trail=AuditTrail()
    for op,status in [("request.created","STARTED"),("validation.failed","FAILED"),("repair.applied","REPAIRED"),("output.accepted","ACCEPTED")]: trail.record(AuditEvent.create("run-1",op,status))
    assert [e.operation for e in trail.events_for_run("run-1")]==["request.created","validation.failed","repair.applied","output.accepted"]
