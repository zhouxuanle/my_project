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

    # Filter out rows containing 'invalid' in any column
    order_item_df = order_item_df[~order_item_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Clean quantity column: remove non-integers and limit to 0 <= quantity < 10000
    if 'quantity' in order_item_df.columns:
        order_item_df['quantity'] = pd.to_numeric(order_item_df['quantity'], errors='coerce')
        order_item_df = order_item_df[order_item_df['quantity'].notna() & (order_item_df['quantity'] >= 0) & (order_item_df['quantity'] < 10000)]
        order_item_df['quantity'] = order_item_df['quantity'].astype(int)

    return order_item_df