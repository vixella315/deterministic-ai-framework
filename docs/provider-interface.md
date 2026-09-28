# Provider Interface

The provider interface is the boundary between the deterministic framework and a probabilistic AI service.

A provider receives a `ProviderRequest` and returns a `ProviderResponse`.

Provider output is **untrusted input**. A provider implementation must not bypass parsing, contract validation, failure classification, repair policy, stop control, or audit.

Future adapters may implement this interface for hosted APIs, local models, or other providers without changing the control layers.

This interface does not claim that model output is true, safe, or deterministic. It standardizes the handoff into the framework.
