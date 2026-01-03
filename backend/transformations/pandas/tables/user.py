"""
User table transformations for the Silver layer.

Handles cleaning and deduplication of user data from raw JSON sources.
"""

import pandas as pd
from typing import List, Dict


def transform_user_data(user_records: List[Dict]) -> pd.DataFrame:
    """
    Complete user data transformation pipeline.

    Args:
        user_records: List of user dictionaries

    Returns:
        Transformed DataFrame
    """
    # Convert list of dicts to DataFrame
    user_df = pd.DataFrame(user_records)

    # Clean text fields: trim whitespace and convert to lowercase
    text_columns = ['real_name', 'company', 'job']
    for col in text_columns:
        if col in user_df.columns:
            user_df[col] = user_df[col].astype(str).str.strip().str.lower()

    # Remove duplicates based on real_name (keep first occurrence)
    if 'real_name' in user_df.columns:
        user_df = user_df.sort_values('real_name')
        user_df = user_df.drop_duplicates(subset=['real_name'], keep='first')
        user_df = user_df.reset_index(drop=True)

    return user_df
