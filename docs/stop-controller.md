# Stop Controller

The stop controller is the framework's fail-closed gate.

## Terminal states

- ACCEPTED
- REPAIRED_AND_ACCEPTED
- REJECTED
- STOPPED
- PROVIDER_FAILURE
- SYSTEM_FAILURE

A repairable failure is **not** an acceptance decision. It requires an authorized repair followed by successful revalidation.

Security, policy, trust, provider, repair, revalidation, and system failures terminate processing.

Unknown failure codes are treated as system failures and therefore fail closed.

The controller does not retry indefinitely and does not invent missing information.
