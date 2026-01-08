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

    # Filter out rows containing 'invalid' in any column FIRST
    products_sku_df = products_sku_df[~products_sku_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Clean quantity column: remove non-integers and limit to 0 <= quantity < 10000
    if 'quantity' in products_sku_df.columns:
        products_sku_df['quantity'] = pd.to_numeric(products_sku_df['quantity'], errors='coerce')
        products_sku_df = products_sku_df[products_sku_df['quantity'].notna() & (products_sku_df['quantity'] >= 0) & (products_sku_df['quantity'] < 10000)]
        products_sku_df['quantity'] = products_sku_df['quantity'].astype(int)

    # Clean price column: remove non-numeric and limit to 0 <= price < 10000
    if 'price' in products_sku_df.columns:
        products_sku_df['price'] = pd.to_numeric(products_sku_df['price'], errors='coerce')
        products_sku_df = products_sku_df[products_sku_df['price'].notna() & (products_sku_df['price'] >= 0) & (products_sku_df['price'] < 10000)]
        products_sku_df['price'] = products_sku_df['price'].astype(float)

    # Remove duplicates based on id, keeping any one row
    if 'id' in products_sku_df.columns:
        products_sku_df = products_sku_df.drop_duplicates(subset=['id'])

    return products_sku_df