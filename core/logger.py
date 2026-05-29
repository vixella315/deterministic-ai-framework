import json
import time


def log_event(event_type: str, payload: dict):
    """
    Structured logging for production-grade observability.

    Every event is recorded as a JSON object so it can be:
    - Parsed by log aggregators
    - Sent to monitoring systems
    - Audited later
    """

    log = {
        "timestamp": time.time(),
        "event_type": event_type,
        "payload": payload
    }

    print(json.dumps(log))
