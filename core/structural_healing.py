def heal(data, schema):
    for key in schema:
        if key not in data:
            data[key] = f"auto_generated_{key}"
    return data
