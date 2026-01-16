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

    # Global encoding cleanup: Remove non-printable characters from all string columns
    for col in user_df.select_dtypes(include=['object']).columns:
        user_df[col] = user_df[col].astype(str).str.replace(r'[^\x20-\x7E]', '', regex=True)

    # Clean text fields: trim whitespace and convert to lowercase
    text_columns = ['real_name', 'company', 'job']
    for col in text_columns:
        if col in user_df.columns:
            user_df[col] = user_df[col].astype(str).str.strip().str.lower()

    # Drop duplicates based on id
    if 'id' in user_df.columns:
        user_df = user_df.drop_duplicates(subset=['id'])

    # Deduplicate by user_id (keep last occurrence)
    if 'user_id' in user_df.columns:
        user_df = user_df.drop_duplicates(subset=['user_id'], keep='last')

    # Filter out rows containing 'invalid' in any column
    user_df = user_df[~user_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Filter sex: ensure it's one of 'male', 'female', or 'other' (case-insensitive, trimmed)
    if 'sex' in user_df.columns:
        user_df = user_df[user_df['sex'].str.strip().str.lower().isin(["male", "female", "other"])]

    # Filter age: ensure it's numeric and within valid range (10-100)
    if 'age' in user_df.columns:
        user_df['age'] = pd.to_numeric(user_df['age'], errors='coerce')
        user_df.loc[~user_df['age'].between(0, 100), 'age'] = None
        user_df['age'] = user_df['age'].astype('Int64')  # Nullable integer

    # Filter birth_of_date: ensure it's a valid date and less than today
    if 'birth_of_date' in user_df.columns:
        user_df['birth_of_date'] = pd.to_datetime(user_df['birth_of_date'], errors='coerce')
        user_df.loc[~(user_df['birth_of_date'] < pd.Timestamp.today()), 'birth_of_date'] = None
    # Remove rows with NaN values created during type casting (after coercion)
    user_df = user_df.dropna()
    # Deduplicate based on real_name, keeping the first in alphabetical order
    if 'real_name' in user_df.columns:
        user_df = user_df.sort_values('real_name')
        user_df = user_df.drop_duplicates(subset=['real_name'], keep='first')
        user_df = user_df.reset_index(drop=True)

    return user_df
