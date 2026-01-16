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

    # Global encoding cleanup: Remove non-printable characters from all string columns
    for col in payment_df.select_dtypes(include=['object']).columns:
        payment_df[col] = payment_df[col].astype(str).str.replace(r'[^\x20-\x7E]', '', regex=True)

    # Filter out rows containing 'invalid' in any column
    payment_df = payment_df[~payment_df.apply(lambda row: row.astype(str).str.lower().str.contains('invalid').any(), axis=1)]

    # Clean text fields: trim whitespace and convert to lowercase
    text_columns = ['provider', 'status']
    for col in text_columns:
        if col in payment_df.columns:
            payment_df[col] = payment_df[col].astype(str).str.strip().str.lower()

    # Filter future-dated timestamps: cap to current date if future
    current_time = pd.Timestamp.now()
    timestamp_columns = ['create_time', 'updated_at', 'delete_time']
    for col in timestamp_columns:
        if col in payment_df.columns:
            payment_df[col] = pd.to_datetime(payment_df[col], errors='coerce')
            # Cap future dates to current time
            payment_df[col] = payment_df[col].apply(lambda x: current_time if pd.notna(x) and x > current_time else x)

    # Clean amount column: convert to numeric and apply range filter
    if 'amount' in payment_df.columns:
        payment_df['amount'] = pd.to_numeric(payment_df['amount'], errors='coerce')
        payment_df.loc[~((payment_df['amount'] >= 0)), 'amount'] = None

    # Remove rows with NaN values created during type casting (after coercion)
    payment_df = payment_df.dropna()

    return payment_df