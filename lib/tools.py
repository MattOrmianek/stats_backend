"""
This module contains tools for the application.
"""

import logging
import time

class timeit:
    """
    A decorator that measures the execution time of a function.
    """

    def __init__(self, name: str, logger: logging.Logger):
        self.name = name
        self.logger = logger  # Store the logger

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            self.logger.info(f"{self.name} took {end_time - start_time} seconds")  # Use the passed logger
            return result
        return wrapper
