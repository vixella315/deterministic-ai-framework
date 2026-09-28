# Testing Strategy

Step 13 establishes unit, integration, failure-matrix, and regression coverage.

Required cases include valid output, missing required data, unexpected properties, malformed JSON, provider failure, security boundaries, audit reconstruction, and the failure taxonomy.

A test file existing is not evidence that it passed. Automated execution and CI reporting are handled in Step 14.

Fail-closed expectation: missing required information without a deterministic source stops; repaired output must pass validation before acceptance.
