import pandas as pd


def clean_addresses(df: pd.DataFrame) -> pd.DataFrame:
    """Clean address data: casing and postal formatting."""
    df['city'] = df['city'].str.title()
    df['country'] = df['country'].str.upper()
    df['postal_code'] = df['postal_code'].astype(str).str.upper()
    return df
