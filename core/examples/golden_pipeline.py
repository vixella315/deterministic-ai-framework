from deterministic.contractual_prompt_factory import ContractualPromptFactory
from deterministic.structural_validator import validate
from deterministic.structural_healing import heal

schema = {
    "title": str,
    "description": str
}

factory = ContractualPromptFactory(schema)
prompt = factory.create("Generate a product listing")

print("PROMPT:")
print(prompt)

ai_output = {
    "title": "AI Product"
}
print("\nSTEP 1 — RAW OUTPUT (FAILURE):")
print(ai_output)

is_valid, error = validate(ai_output, schema)
print("\nSTEP 2 — VALIDATION RESULT:")
print("Valid:", is_valid, "| Error:", error)

if not is_valid:
    print("\nSTEP 3 — HEALING TRIGGERED")
    ai_output = heal(ai_output, schema)

print("\nSTEP 4 — HEALED OUTPUT:")
print(ai_output)

is_valid, error = validate(ai_output, schema)
print("\nSTEP 5 — FINAL VALIDATION:")
print("Valid:", is_valid, "| Error:", error)
