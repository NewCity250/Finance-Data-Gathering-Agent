import os
import pandas as pd
from agent.sec import cik_from_ticker, get_companyfacts, extract_usgaap_facts
from agent.prices import stooq_prices

USGAAP_TAGS = [
    "Revenues", "NetIncomeLoss",
    "CashAndCashEquivalentsAtCarryingValue",
    "CapitalExpenditures", "DepreciationDepletionAndAmortization"
]

TICKERS = ["XOM", "CVX"]  # Exxon, Chevron

def ensure_dirs():
    os.makedirs("data", exist_ok=True)

def run_for_ticker(tkr):
    cik = cik_from_ticker(tkr)
    facts = get_companyfacts(cik)
    df = extract_usgaap_facts(facts, USGAAP_TAGS)
    df.to_csv(f"data/{tkr}_facts.csv", index=False)

    px = stooq_prices(tkr)
    px.to_csv(f"data/{tkr}_prices.csv", index=False)

    print(f"Saved: data/{tkr}_facts.csv, data/{tkr}_prices.csv")

if __name__ == "__main__":
    ensure_dirs()
    for t in TICKERS:
        run_for_ticker(t)
    print("Done.")
