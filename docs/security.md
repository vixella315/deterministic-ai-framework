# Security Layer

The security layer is a boundary, not a guarantee of safety.

It enforces bounded prompt/output sizes, rejects selected control characters, and provides fail-closed JSON parsing.

## Trust assumptions

External content and model output are untrusted. Successful parsing does not establish truth or safety.

## Secrets

Credentials and API keys must be supplied through environment variables or an appropriate secret manager. They must not be committed to source or written to audit logs.

## Prompt injection

Prompt injection is treated as an input-security concern. The framework must keep instructions, data, and model output conceptually separate and must validate model-produced structured data before downstream use. This layer does not claim to detect every injection technique.

## Future hardening

Dependency scanning, CI security checks, authentication/authorization, redaction policy, sandboxing, rate limiting, and provider-specific security controls remain separate tasks.
