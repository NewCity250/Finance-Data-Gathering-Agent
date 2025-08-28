import os, requests, pandas as pd

BASE = "https://data.sec.gov"
UA = os.environ.get("SEC_USER_AGENT", "your-app-name ([email protected])")  # REQUIRED by SEC

def get_cik_map():
    url = "https://www.sec.gov/files/company_tickers.json"
    r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    return r.json()

def cik_from_ticker(ticker: str) -> str:
    m = get_cik_map()
    for _, v in m.items():
        if v["ticker"].lower() == ticker.lower():
            return str(v["cik_str"]).zfill(10)
    raise ValueError(f"Ticker not found: {ticker}")

def get_companyfacts(cik: str) -> dict:
    url = f"{BASE}/api/xbrl/companyfacts/CIK{cik}.json"
    r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    return r.json()

def extract_usgaap_facts(facts: dict, tags: list[str]) -> pd.DataFrame:
    rows = []
    fdict = facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        tagdata = fdict.get(tag, {})
        for unit, items in tagdata.get("units", {}).items():
            for it in items:
                rows.append({
                    "tag": tag,
                    "fy": it.get("fy"),
                    "fp": it.get("fp"),
                    "end": it.get("end"),
                    "val": it.get("val"),
                    "unit": unit
                })
    df = pd.DataFrame(rows).dropna(subset=["fy"])
    if not df.empty:
        df = df.sort_values(["tag", "end"])
    return df
