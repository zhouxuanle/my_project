"""
Product table transformations for the Silver layer.

Handles cleaning and deduplication of product data from raw JSON sources.
"""

import pandas as pd
from typing import List, Dict


def transform_product_data(product_records: List[Dict]) -> pd.DataFrame:
    """
    Complete product data transformation pipeline.

    Args:
        product_records: List of product dictionaries

    Returns:
        Transformed DataFrame
    """
    # Convert list of dicts to DataFrame
    product_df = pd.DataFrame(product_records)

    # Filter out rows containing 'invalid' in any column
    product_df = product_df[~product_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Clean text fields: trim whitespace and convert to lowercase
    text_columns = ['description', 'name']
    for col in text_columns:
        if col in product_df.columns:
            product_df[col] = product_df[col].astype(str).str.strip().str.lower()

    # Remove duplicates based on id
    if 'id' in product_df.columns:
        product_df = product_df.drop_duplicates(subset=['id'])

    return product_df