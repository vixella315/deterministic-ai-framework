def validate(data, schema):
    for key in schema:
        if key not in data:
            return False, f"Missing field: {key}"
    return True, "Valid"
