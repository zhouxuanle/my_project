"""
Order table transformations for the Silver layer.

Handles cleaning and deduplication of order data from raw JSON sources.
"""

import pandas as pd
from typing import List, Dict


def transform_order_data(order_records: List[Dict]) -> pd.DataFrame:
    """
    Complete order data transformation pipeline.

    Args:
        order_records: List of order dictionaries

    Returns:
        Transformed DataFrame
    """
    # Convert list of dicts to DataFrame
    order_df = pd.DataFrame(order_records)

    # Filter out rows containing 'invalid' in any column
    order_df = order_df[~order_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Remove rows with NaN values created during type casting (after coercion)
    order_df = order_df.dropna()

    # Remove duplicates based on payment_id
    if 'payment_id' in order_df.columns:
        order_df = order_df.drop_duplicates(subset=['payment_id'])

    return order_df