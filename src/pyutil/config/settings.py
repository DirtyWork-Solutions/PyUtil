import json
import yaml
from omegaconf import OmegaConf
from src.pyutil.config.loader import ConfigLoader
from loguru import logger

class Settings:
    def __init__(self, config_paths=None, defaults=None):
        self.config_loader = ConfigLoader(config_paths)
        self.defaults = defaults or {}
        self.config = OmegaConf.create(self.defaults)
        logger.info("Settings initialized with defaults: {}", self.defaults)

    def load(self):
        """Load and merge configurations."""
        loaded_config = self.config_loader.load()
        self.config = OmegaConf.merge(self.config, loaded_config)
        logger.info("Configuration loaded and merged: {}", self.config)

    def get(self, key, default=None):
        """Retrieve a setting value."""
        return OmegaConf.select(self.config, key, default=default)

    def set(self, key, value):
        """Update a setting value."""
        OmegaConf.update(self.config, key, value)
        logger.info("Updated configuration key '{}' to '{}'", key, value)

    def save(self, path, format="yaml"):
        """Save current settings to a file."""
        with open(path, 'w') as f:
            container = OmegaConf.to_container(self.config)
            if format == "yaml":
                yaml.dump(container, f)
            elif format == "json":
                json.dump(container, f, indent=4)
        logger.info("Configuration saved to {}", path)
