# Failure Taxonomy

Failures are classified into **ACCEPT**, **REPAIR**, or **STOP**.

REPAIR means only that an explicit repair policy may permit a deterministic transformation. It never authorizes fabrication or inference.

Unknown failures fail closed. Security, policy, trust, provider, repair, revalidation, and system failures stop processing.

A repaired result must pass validation again before acceptance.

The complete initial taxonomy is represented by `FailureCode` in the validation package and is machine-readable.
