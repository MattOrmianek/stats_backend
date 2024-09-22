"""
This module contains functions to read data from a file.
"""

import logging
import pandas as pd
from fastapi import HTTPException


def read_data(file_path: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Read data from a file.
    """
    try:
        return pd.read_excel(file_path, engine="openpyxl")  # Specify the engine
    except Exception as error:
        logger.error("Error reading data from file: %s", str(error), exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An error occurred while reading the file: {str(error)}"
        ) from error
