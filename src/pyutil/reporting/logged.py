"""
This module is used to log messages. It uses either; the loguru or python native library to log messages.
"""

from loguru import logger
from src.pyutil.config import settings
import sys

class Logged:
    """Manages structured logging for PyUtil using Loguru, configured via pyutil.config."""

    def __init__(self):
        self._configure_logging()

    def _configure_logging(self):
        """Loads logging settings from pyutil.config and applies them to Loguru."""
        log_config = settings.get("logging", {}) # Load logging settings from config

        # Default log level and format
        log_level = log_config.get("level", "INFO").upper()
        log_format = log_config.get("format", "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

        # Remove default handlers before configuring custom ones
        logger.remove()

        # Console Logging
        if log_config.get("console", True):
            logger.add(sys.stderr, format=log_format, level=log_level, enqueue=True, colorize=True)

        # File Logging
        log_file = log_config.get("file_path", "logs/pyutil.log")
        if log_config.get("file_logging", False):
            logger.add(log_file, rotation="10MB", retention="7 days", level=log_level, format=log_format, enqueue=True)

    def get_logger(self):
        """Returns the configured Loguru logger."""
        return logger

# Instantiate logging manager
log_manager = Logged()
log = log_manager.get_logger()
