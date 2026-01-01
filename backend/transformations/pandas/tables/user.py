"""
User table transformations for the Silver layer.

Handles cleaning and deduplication of user data from raw JSON sources.
"""

import pandas as pd


def transform_user_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Complete user data transformation pipeline.

    Args:
        raw_data: Raw DataFrame containing nested user data

    Returns:
        Transformed DataFrame
    """
    # Extract user data from nested structure
    if 'user' not in raw_data.columns:
        raise ValueError("Raw data must contain 'user' column with nested user data")
    user_df = pd.json_normalize(raw_data['user'])

    # Clean text fields: trim whitespace and convert to lowercase
    text_columns = ['real_name', 'company', 'job']
    for col in text_columns:
        if col in user_df.columns:
            user_df[col] = user_df[col].astype(str).str.strip().str.lower()

    # Remove duplicates based on real_name (keep first occurrence)
    if 'real_name' not in user_df.columns:
        raise ValueError("Deduplication column 'real_name' not found in DataFrame")
    user_df = user_df.sort_values('real_name')
    user_df = user_df.drop_duplicates(subset=['real_name'], keep='first')
    user_df = user_df.reset_index(drop=True)

    return user_df
