"""
Wishlist table transformations for the Silver layer.

Handles cleaning and deduplication of wishlist data from raw JSON sources.
"""

import pandas as pd
from typing import List, Dict


def transform_wishlist_data(wishlist_records: List[Dict]) -> pd.DataFrame:
    """
    Complete wishlist data transformation pipeline.

    Args:
        wishlist_records: List of wishlist dictionaries

    Returns:
        Transformed DataFrame
    """
    # Convert list of dicts to DataFrame
    wishlist_df = pd.DataFrame(wishlist_records)

    # Filter out rows containing 'invalid' in any column
    wishlist_df = wishlist_df[~wishlist_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Explicit timestamp casting for datetime columns
    timestamp_columns = ['create_time', 'delete_time']
    for col in timestamp_columns:
        if col in wishlist_df.columns:
            wishlist_df[col] = pd.to_datetime(wishlist_df[col], errors='coerce')

    # Remove rows with NaN values created during type casting (after coercion)
    wishlist_df = wishlist_df.dropna()

    # Remove duplicates based on user_id
    if 'user_id' in wishlist_df.columns:
        wishlist_df = wishlist_df.drop_duplicates(subset=['user_id'])

    return wishlist_df