"""
This module provides a logger configuration for the application.
"""

from logging.handlers import RotatingFileHandler
import logging
import colorlog

logger = None


def setup_logger(name):
    """
    Setup the logger with the given name.
    """
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # File Handler
    file_handler = RotatingFileHandler("backend.log", maxBytes=50 * 1024 * 1024, backupCount=50)
    file_handler.setLevel(logging.DEBUG)

    # Formatter
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(filename)s:%(lineno)d - "
        "%(funcName)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    _logger.addHandler(console_handler)
    _logger.addHandler(file_handler)

    return _logger


logger = setup_logger("logger")
