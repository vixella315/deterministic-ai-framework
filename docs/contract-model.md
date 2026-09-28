# Contract Model

The JSON Schema layer defines the external structural contract used by later validation stages.

## Rules

1. JSON Schema is the canonical external contract language.
2. The contract defines structure; it does not establish factual truth.
3. Schema version is explicit.
4. Unknown top-level properties are rejected.
5. Validation behavior belongs to the validation layer, not the schema loader.
6. A schema is loaded as data and must not be silently mutated.

The canonical Asset contract is currently version 1.0.
