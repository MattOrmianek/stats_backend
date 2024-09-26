"""
This module contains functions for generating random data points.
"""

import random
from lib.tools import timeit
from lib.logger.logger_config import logger


@timeit("generate_data", logger)
def generate_data(num_points: int, min_value: float, max_value: float) -> list[tuple[float, float]]:
    """
    Generate a list of random data points.
    """
    logger.info(
        "Generating %d random data points between %f and %f", num_points, min_value, max_value
    )

    def generate_point() -> tuple[float, float]:
        """Generate a single random point."""
        return (random.uniform(min_value, max_value), random.uniform(min_value, max_value))

    data = [generate_point() for _ in range(num_points)]
    return data
