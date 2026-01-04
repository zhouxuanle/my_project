"""
Subcategory table transformations for the Silver layer.

Handles cleaning and deduplication of subcategory data from raw JSON sources.
"""

import pandas as pd
from typing import List, Dict


def transform_subcategory_data(subcategory_records: List[Dict]) -> pd.DataFrame:
    """
    Complete subcategory data transformation pipeline.

    Args:
        subcategory_records: List of subcategory dictionaries

    Returns:
        Transformed DataFrame
    """
    # Convert list of dicts to DataFrame
    subcategory_df = pd.DataFrame(subcategory_records)

    # Filter out rows containing 'invalid' in any column
    subcategory_df = subcategory_df[~subcategory_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Clean text fields: trim whitespace and convert to lowercase
    text_columns = ['description', 'name']
    for col in text_columns:
        if col in subcategory_df.columns:
            subcategory_df[col] = subcategory_df[col].astype(str).str.strip().str.lower()

    # Remove duplicates based on id
    if 'id' in subcategory_df.columns:
        subcategory_df = subcategory_df.drop_duplicates(subset=['id'])

    return subcategory_df