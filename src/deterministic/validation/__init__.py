"""Contract validation engine and failure taxonomy."""

from .engine import Validator
from .failures import FailureAction, FailureCode, FailureRule, get_failure_rule

__all__ = ["Validator", "FailureAction", "FailureCode", "FailureRule", "get_failure_rule"]
