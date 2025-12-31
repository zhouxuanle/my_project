import pandas as pd

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def clean_users(df: pd.DataFrame) -> pd.DataFrame:
    """Clean user data: normalize email, phone, age, and dates; drop missing ids."""
    df['email'] = df['email'].str.lower().str.strip()
    df['email'] = df[df['email'].str.match(EMAIL_REGEX, na=False)]['email']
    df['phone'] = df['phone'].str.replace(r'\D', '', regex=True)
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df = df[(df['age'] >= 13) & (df['age'] <= 120)]
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    return df.dropna(subset=['user_id'])


def calculate_quality_score(df: pd.DataFrame) -> pd.Series:
    """Score rows on completeness/format; range 0-100."""
    score = pd.Series([100] * len(df))
    score -= df['email'].isna().astype(int) * 20
    score -= df['phone'].isna().astype(int) * 15
    score -= df['age'].isna().astype(int) * 10
    score -= (~df['email'].str.match(EMAIL_REGEX, na=False)).astype(int) * 15
    return score.clip(lower=0, upper=100)
