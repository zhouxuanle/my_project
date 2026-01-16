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

    # Global encoding cleanup: Remove non-printable characters from all string columns
    for col in product_df.select_dtypes(include=['object']).columns:
        product_df[col] = product_df[col].astype(str).str.replace(r'[^\x20-\x7E]', '', regex=True)

    # Filter out rows containing 'invalid' in any column
    product_df = product_df[~product_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Clean text fields: trim whitespace and convert to lowercase
    text_columns = ['description', 'name']
    for col in text_columns:
        if col in product_df.columns:
            product_df[col] = product_df[col].astype(str).str.strip().str.lower()

    # Filter future-dated timestamps: cap to current date if future
    current_time = pd.Timestamp.now()
    timestamp_columns = ['create_time', 'updated_at', 'delete_time']
    for col in timestamp_columns:
        if col in product_df.columns:
            product_df[col] = pd.to_datetime(product_df[col], errors='coerce')
            # Cap future dates to current time
            product_df[col] = product_df[col].apply(lambda x: current_time if pd.notna(x) and x > current_time else x)

    # Remove rows with NaN values created during type casting (after coercion)
    product_df = product_df.dropna()

    # Remove duplicates based on id
    if 'id' in product_df.columns:
        product_df = product_df.drop_duplicates(subset=['id'])

    return product_df