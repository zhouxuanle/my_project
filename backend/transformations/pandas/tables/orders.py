import pandas as pd


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Clean order data: types and required fields."""
    df['order_id'] = df['order_id'].astype(str)
    df['user_id'] = df['user_id'].astype(str)
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    return df.dropna(subset=['order_id', 'user_id'])
