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

print("\nRAW OUTPUT:")
print(ai_output)

is_valid, error = validate(ai_output, schema)
print("\nVALIDATION:")
print(is_valid, error)

if not is_valid:
    ai_output = heal(ai_output, schema)

print("\nHEALED OUTPUT:")
print(ai_output)

is_valid, error = validate(ai_output, schema)
print("\nFINAL VALIDATION:")
print(is_valid, error)
