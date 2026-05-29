from deterministic.contractual_prompt_factory import ContractualPromptFactory
from deterministic.structural_validator import validate
from deterministic.structural_healing import heal


# Define schema
schema = {
    "title": str,
    "description": str
}

# Step 1: Generate prompt
factory = ContractualPromptFactory(schema)
prompt = factory.create("Generate a product listing")

print("PROMPT:")
print(prompt)


# Step 2: Simulated AI output (broken on purpose)
ai_output = {
    "title": "AI Product"
    # missing "description"
}

print("\nRAW OUTPUT:")
print(ai_output)


# Step 3: Validate
is_valid, error = validate(ai_output, schema)
print("\nVALIDATION:")
print(is_valid, error)


# Step 4: Heal
if not is_valid:
    ai_output = heal(ai_output, schema)

print("\nHEALED OUTPUT:")
print(ai_output)


# Step 5: Validate again
is_valid, error = validate(ai_output, schema)
print("\nFINAL VALIDATION:")
print(is_valid, error)
