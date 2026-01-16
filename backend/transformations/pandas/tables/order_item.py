"""
Order item table transformations for the Silver layer.

Handles cleaning of order item data from raw JSON sources.
"""

import pandas as pd
from typing import List, Dict


def transform_order_item_data(order_item_records: List[Dict]) -> pd.DataFrame:
    """
    Complete order item data transformation pipeline.

    Args:
        order_item_records: List of order item dictionaries

    Returns:
        Transformed DataFrame
    """
    # Convert list of dicts to DataFrame
    order_item_df = pd.DataFrame(order_item_records)

    # Global encoding cleanup: Remove non-printable characters from all string columns
    for col in order_item_df.select_dtypes(include=['object']).columns:
        order_item_df[col] = order_item_df[col].astype(str).str.replace(r'[^\x20-\x7E]', '', regex=True)

    # Filter out rows containing 'invalid' in any column
    order_item_df = order_item_df[~order_item_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Clean quantity column: convert to numeric, apply range filter
    if 'quantity' in order_item_df.columns:
        order_item_df['quantity'] = pd.to_numeric(order_item_df['quantity'], errors='coerce')
        order_item_df.loc[~((order_item_df['quantity'] >= 0) & (order_item_df['quantity'] < 10000)), 'quantity'] = None
        order_item_df['quantity'] = order_item_df['quantity'].astype('Int64')  # Nullable integer type

    # Explicit type casting for all ID columns to string
    id_columns = [col for col in order_item_df.columns if 'id' in col.lower()]
    for col in id_columns:
        if col in order_item_df.columns:
            order_item_df[col] = order_item_df[col].astype(str)

    # Explicit timestamp casting for datetime columns
    timestamp_columns = ['create_time', 'updated_at']
    for col in timestamp_columns:
        if col in order_item_df.columns:
            order_item_df[col] = pd.to_datetime(order_item_df[col], errors='coerce')

    # Remove rows with NaN values created during type casting (after coercion)
    order_item_df = order_item_df.dropna()

    return order_item_df