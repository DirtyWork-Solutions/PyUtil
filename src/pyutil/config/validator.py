
from cerberus import Validator

class ConfigValidator:
    def __init__(self, schema):
        self.schema = schema
        self.validator = Validator(schema)

    def validate(self, config):
        """Validate a configuration dictionary against the schema."""
        if not self.validator.validate(config):
            raise ValueError(f"Invalid config: {self.validator.errors}")