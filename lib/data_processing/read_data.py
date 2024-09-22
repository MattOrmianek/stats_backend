"""
This module contains functions to read data from a file.
"""

import pandas as pd

def read_data(file_path: str) -> pd.DataFrame:
    """
    Read data from a file.
    """
    return pd.read_excel(file_path)