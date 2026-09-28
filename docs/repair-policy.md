# Safe Repair Policy

The repair engine is deliberately conservative.

## Allowed principle

A repair may change structure only when the transformation is deterministic, explicitly authorized, and semantics-preserving.

## Prohibited

The engine must not:

- invent missing facts;
- guess values;
- create citations or sources;
- infer unsupported information;
- silently replace ambiguous values;
- treat successful execution as successful validation.

## Current implementation

The first supported repair is explicit removal of an identified unexpected property.

Missing, null, empty, enum, range, and other semantic failures stop unless a later policy provides a deterministic source and transformation.

Every repaired result must be revalidated before acceptance.
