# Audit Model

The audit layer records control-plane events so a run can be reconstructed without automatically storing raw prompts, model output, secrets, or sensitive content.

Each event has a unique `event_id` and a `run_id` for correlation.

Core fields include timestamp, operation, status, framework/schema versions, provider/model identity when available, failure codes, repair actions, reason, and optional content hashes.

The initial implementation is append-only in memory. Durable storage, retention, export, redaction policy, and tamper-evidence are later deployment concerns.

Hashes provide content identity without requiring the content itself to be stored. A hash is not a proof that content is true or safe.
