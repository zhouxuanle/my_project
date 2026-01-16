"""
Products SKU table transformations for the Silver layer.

Handles cleaning and deduplication of products SKU data from raw JSON sources.
"""

import pandas as pd
from typing import List, Dict


def transform_products_sku_data(products_sku_records: List[Dict]) -> pd.DataFrame:
    """
    Complete products SKU data transformation pipeline.

    Args:
        products_sku_records: List of products SKU dictionaries

    Returns:
        Transformed DataFrame
    """
    # Convert list of dicts to DataFrame
    products_sku_df = pd.DataFrame(products_sku_records)

    # Global encoding cleanup: Remove non-printable characters from all string columns
    for col in products_sku_df.select_dtypes(include=['object']).columns:
        products_sku_df[col] = products_sku_df[col].astype(str).str.replace(r'[^\x20-\x7E]', '', regex=True)

    # Filter out rows containing 'invalid' in any column FIRST
    products_sku_df = products_sku_df[~products_sku_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Clean quantity column: convert to numeric, apply range filter
    if 'quantity' in products_sku_df.columns:
        products_sku_df['quantity'] = pd.to_numeric(products_sku_df['quantity'], errors='coerce')
        products_sku_df.loc[~((products_sku_df['quantity'] >= 0) & (products_sku_df['quantity'] < 10000)), 'quantity'] = None
        products_sku_df['quantity'] = products_sku_df['quantity'].astype('Int64')  # Nullable integer type

    # Clean price column: convert to numeric, apply range filter
    if 'price' in products_sku_df.columns:
        products_sku_df['price'] = pd.to_numeric(products_sku_df['price'], errors='coerce')
        products_sku_df.loc[~((products_sku_df['price'] >= 0) & (products_sku_df['price'] < 10000)), 'price'] = None
        products_sku_df['price'] = products_sku_df['price'].astype('float64')

    # Explicit type casting for all ID columns to string
    id_columns = [col for col in products_sku_df.columns if 'id' in col.lower()]
    for col in id_columns:
        if col in products_sku_df.columns:
            products_sku_df[col] = products_sku_df[col].astype(str)

    # Explicit timestamp casting for datetime columns
    timestamp_columns = ['create_time', 'delete_time']
    for col in timestamp_columns:
        if col in products_sku_df.columns:
            products_sku_df[col] = pd.to_datetime(products_sku_df[col], errors='coerce')

    # Remove rows with NaN values created during type casting (after coercion)
    products_sku_df = products_sku_df.dropna()

    # Remove duplicates based on id, keeping any one row
    if 'id' in products_sku_df.columns:
        products_sku_df = products_sku_df.drop_duplicates(subset=['id'])

    return products_sku_df