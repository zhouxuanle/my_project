"""
Payment table transformations for the Silver layer.

Handles cleaning of payment data from raw JSON sources.
"""

import pandas as pd
from typing import List, Dict


def transform_payment_data(payment_records: List[Dict]) -> pd.DataFrame:
    """
    Complete payment data transformation pipeline.

    Args:
        payment_records: List of payment dictionaries

    Returns:
        Transformed DataFrame
    """
    # Convert list of dicts to DataFrame
    payment_df = pd.DataFrame(payment_records)

    # Filter out rows containing 'invalid' in any column
    payment_df = payment_df[~payment_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Clean text fields: trim whitespace and convert to lowercase
    text_columns = ['provider', 'status']
    for col in text_columns:
        if col in payment_df.columns:
            payment_df[col] = payment_df[col].astype(str).str.strip().str.lower()

    # Clean amount column: remove non-numeric and limit to 0 <= amount < 10000
    if 'amount' in payment_df.columns:
        payment_df['amount'] = pd.to_numeric(payment_df['amount'], errors='coerce')
        payment_df = payment_df[payment_df['amount'].notna() & (payment_df['amount'] >= 0) & (payment_df['amount'] < 10000)]

    return payment_df