"""
Address table transformations for the Silver layer.

Handles cleaning and deduplication of address data from raw JSON sources.
"""

import pandas as pd
from typing import List, Dict


def transform_address_data(address_records: List[Dict]) -> pd.DataFrame:
    """
    Complete address data transformation pipeline.

    Args:
        address_records: List of address dictionaries

    Returns:
        Transformed DataFrame
    """
    # Convert list of dicts to DataFrame
    address_df = pd.DataFrame(address_records)

    # Filter out rows containing 'invalid' in any column
    address_df = address_df[~address_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Clean text fields: trim whitespace and convert to lowercase
    text_columns = ['address_line', 'city', 'country', 'title']
    for col in text_columns:
        if col in address_df.columns:
            address_df[col] = address_df[col].astype(str).str.strip().str.lower()

    # Filter future-dated timestamps: cap to current date if future
    current_time = pd.Timestamp.now()
    timestamp_columns = ['create_time', 'delete_time']
    for col in timestamp_columns:
        if col in address_df.columns:
            address_df[col] = pd.to_datetime(address_df[col], errors='coerce')
            # Cap future dates to current time
            address_df[col] = address_df[col].apply(lambda x: current_time if pd.notna(x) and x > current_time else x)

    # Remove rows with NaN values created during type casting (after coercion)
    address_df = address_df.dropna()

    # Remove duplicates based on user_id
    if 'user_id' in address_df.columns:
        address_df = address_df.drop_duplicates(subset=['user_id'])

    return address_df