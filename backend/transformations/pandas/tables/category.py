"""
Category table transformations for the Silver layer.

Handles cleaning and deduplication of category data from raw JSON sources.
"""

import pandas as pd
from typing import List, Dict


def transform_category_data(category_records: List[Dict]) -> pd.DataFrame:
    """
    Complete category data transformation pipeline.

    Args:
        category_records: List of category dictionaries

    Returns:
        Transformed DataFrame
    """
    # Convert list of dicts to DataFrame
    category_df = pd.DataFrame(category_records)

    # Filter out rows containing 'invalid' in any column
    category_df = category_df[~category_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Clean text fields: trim whitespace and convert to lowercase
    text_columns = ['description', 'name']
    for col in text_columns:
        if col in category_df.columns:
            category_df[col] = category_df[col].astype(str).str.strip().str.lower()

    # Remove rows with NaN values created during type casting (after coercion)
    category_df = category_df.dropna()

    # Remove duplicates based on id
    if 'id' in category_df.columns:
        category_df = category_df.drop_duplicates(subset=['id'])

    return category_df