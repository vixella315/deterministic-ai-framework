class Orchestrator:
    def __init__(self, factory, validator, healer):
        self.factory = factory
        self.validator = validator
        self.healer = healer

    def run(self, prompt, schema):
        raw = self.factory.generate(prompt)
        
        if not self.validator.validate(raw, schema):
            raw = self.healer.heal(raw, schema)
        
        return raw
