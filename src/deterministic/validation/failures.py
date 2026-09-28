"""Controlled failure taxonomy and handling policy."""
from dataclasses import dataclass
from enum import Enum

class FailureAction(str, Enum):
    ACCEPT="ACCEPT"; REPAIR="REPAIR"; STOP="STOP"

class FailureCode(str, Enum):
    PARSE_ERROR="PARSE_ERROR"; SCHEMA_ERROR="SCHEMA_ERROR"; REQUIRED_FIELD_MISSING="REQUIRED_FIELD_MISSING"; TYPE_ERROR="TYPE_ERROR"; NULL_NOT_ALLOWED="NULL_NOT_ALLOWED"; EMPTY_VALUE="EMPTY_VALUE"; INVALID_ENUM="INVALID_ENUM"; VALUE_OUT_OF_RANGE="VALUE_OUT_OF_RANGE"; INVALID_FORMAT="INVALID_FORMAT"; UNEXPECTED_PROPERTY="UNEXPECTED_PROPERTY"; NESTED_STRUCTURE_ERROR="NESTED_STRUCTURE_ERROR"; POLICY_VIOLATION="POLICY_VIOLATION"; SECURITY_VIOLATION="SECURITY_VIOLATION"; UNTRUSTED_CONTENT="UNTRUSTED_CONTENT"; PROVIDER_ERROR="PROVIDER_ERROR"; PROVIDER_TIMEOUT="PROVIDER_TIMEOUT"; PROVIDER_UNAVAILABLE="PROVIDER_UNAVAILABLE"; REPAIR_FAILED="REPAIR_FAILED"; REVALIDATION_FAILED="REVALIDATION_FAILED"; SYSTEM_ERROR="SYSTEM_ERROR"

@dataclass(frozen=True)
class FailureRule:
    code: FailureCode
    action: FailureAction
    default_repairable: bool
    reason: str

_REPAIRABLE={FailureCode.REQUIRED_FIELD_MISSING,FailureCode.TYPE_ERROR,FailureCode.NULL_NOT_ALLOWED,FailureCode.EMPTY_VALUE,FailureCode.INVALID_FORMAT,FailureCode.UNEXPECTED_PROPERTY,FailureCode.NESTED_STRUCTURE_ERROR}
FAILURE_RULES={code: FailureRule(code, FailureAction.REPAIR if code in _REPAIRABLE else FailureAction.STOP, code in _REPAIRABLE, "Potentially repairable only under explicit policy; never invent facts." if code in _REPAIRABLE else "Failure must stop processing.") for code in FailureCode}

def get_failure_rule(code: str|FailureCode)->FailureRule:
    try: normalized=code if isinstance(code,FailureCode) else FailureCode(code)
    except ValueError: return FailureRule(FailureCode.SYSTEM_ERROR,FailureAction.STOP,False,"Unknown failure codes fail closed.")
    return FAILURE_RULES[normalized]
