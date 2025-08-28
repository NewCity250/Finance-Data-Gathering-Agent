import pandas as pd

def stooq_prices(ticker: str):
    # Stooq uses .us for US tickers
    url = f"https://stooq.com/q/d/l/?s={ticker.lower()}.us&i=d"
    df = pd.read_csv(url)  # date, open, high, low, close, volume
    return df
