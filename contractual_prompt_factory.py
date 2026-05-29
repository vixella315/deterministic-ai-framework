class ContractualPromptFactory:
    def __init__(self, schema):
        self.schema = schema

    def create(self, goal):
        return f"""
        GOAL: {goal}
        REQUIRED FIELDS: {list(self.schema.keys())}
        OUTPUT MUST BE JSON ONLY
        """
