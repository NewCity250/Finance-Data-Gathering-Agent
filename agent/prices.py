import pandas as pd

def stooq_prices(ticker: str, start: str = "2000-01-01"):
    """
    Download daily prices from Stooq and keep rows on/after `start` (YYYY-MM-DD).
    """
    url = f"https://stooq.com/q/d/l/?s={ticker.lower()}.us&i=d"
    df = pd.read_csv(url)  # columns: Date,Open,High,Low,Close,Volume
    # Parse and filter by date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    if start:
        df = df[df["Date"] >= pd.to_datetime(start)]
    # Write Date back as string for clean CSVs
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    return df.reset_index(drop=True)
