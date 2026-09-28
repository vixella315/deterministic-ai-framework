# Validation Engine

The validation engine is the enforcement point between raw structured data and later repair or acceptance.

## Behavior

- Uses JSON Schema Draft 2020-12.
- Uses explicit format checking.
- Reports all discovered schema errors rather than stopping at the first error.
- Converts library-specific validation failures into the framework's ErrorDetail model.
- Produces a ValidationResult.
- Does not mutate input.
- Does not repair data.
- Does not infer missing facts.

## Boundary

Validation answers:

> "Does this data satisfy the current contract?"

It does not answer:

> "Is this information true?"

It also does not decide whether a failure should be repaired. Repair policy is a later step.
