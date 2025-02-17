import json
import yaml
from omegaconf import OmegaConf

from src.pyutil.config.loader import ConfigLoader

from cryptography.fernet import Fernet
import os

class Settings:
    def __init__(self, config_paths=None, defaults=None):
        self.config_loader = ConfigLoader(config_paths)
        self.defaults = defaults or {}
        self.config = OmegaConf.create(self.defaults)

    def load(self):
        """Load and merge configurations."""
        loaded_config = self.config_loader.load()
        self.config = OmegaConf.merge(self.config, loaded_config)

    def get(self, key, default=None):
        """Retrieve a setting value."""
        return OmegaConf.select(self.config, key, default=default)

    def set(self, key, value):
        """Update a setting value."""
        OmegaConf.update(self.config, key, value)

    def save(self, path, format="yaml"):
        """Save current settings to a file."""
        with open(path, 'w') as f:
            if format == "yaml" or format == 'yml':
                yaml.dump(OmegaConf.to_container(self.config), f)
            elif format == "json":
                json.dump(OmegaConf.to_container(self.config), f, indent=4)

class HierarchicalSettings(Settings):
    def __init__(self, global_config, module_config=None, user_config=None):
        super().__init__(config_paths=[global_config])
        self.module_config = module_config
        self.user_config = user_config

    def load(self):
        """Load configurations with precedence: User > Module > Global"""
        super().load()
        if self.module_config:
            module_data = ConfigLoader([self.module_config]).load()
            self.config = OmegaConf.merge(self.config, module_data)

        if self.user_config:
            user_data = ConfigLoader([self.user_config]).load()
            self.config = OmegaConf.merge(self.config, user_data)



class SecureConfig(Settings):
    def __init__(self, config_paths, encryption_key=None):
        super().__init__(config_paths)
        self.encryption_key = encryption_key or os.getenv("CONFIG_ENCRYPTION_KEY")

    def encrypt_value(self, value):
        """Encrypt a configuration value."""
        f = Fernet(self.encryption_key)
        return f.encrypt(value.encode()).decode()

    def decrypt_value(self, encrypted_value):
        """Decrypt an encrypted configuration value."""
        f = Fernet(self.encryption_key)
        return f.decrypt(encrypted_value.encode()).decode()

    def get_secure(self, key, default=None):
        """Retrieve and decrypt a setting."""
        encrypted_value = self.get(key, default)
        return self.decrypt_value(encrypted_value) if encrypted_value else default

    def set_secure(self, key, value):
        """Encrypt and store a setting."""
        self.set(key, self.encrypt_value(value))
