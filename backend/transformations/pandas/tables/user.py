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

    # Drop duplicates based on id
    if 'id' in user_df.columns:
        user_df = user_df.drop_duplicates(subset=['id'])

    # Filter out rows containing 'invalid' in any column
    user_df = user_df[~user_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Filter age: ensure it's numeric and within valid range (10-100)
    if 'age' in user_df.columns:
        user_df['age'] = pd.to_numeric(user_df['age'], errors='coerce')
        user_df = user_df[user_df['age'].between(10, 100)]
        user_df['age'] = user_df['age'].astype(int)

    # Remove duplicates based on real_name (keep first occurrence)
    if 'real_name' in user_df.columns:
        user_df = user_df.sort_values('real_name')
        user_df = user_df.drop_duplicates(subset=['real_name'], keep='first')
        user_df = user_df.reset_index(drop=True)

    return user_df
