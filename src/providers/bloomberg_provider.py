
import json
from pathlib import Path


BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

ACCESS_MODE = "APPROVED_SAMPLE"

SAMPLE_PATH = (
    Path(__file__).resolve().parents[2]
    / "data/sample/bloomberg_reference_sample.json"
)


def fetch_raw_bloomberg_history(identifier):
    with open(SAMPLE_PATH, encoding="utf-8") as file:
        data = json.load(file)

    for series in data["series"]:
        if series["provider_identifier"] == identifier:
            return series

    raise ValueError(f"No sample data found for {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    if raw_data["canonical_ticker"] != canonical_ticker:
        raise ValueError("Canonical ticker mismatch")

    rows = []

    for observation in raw_data["observations"]:
        rows.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })

    return rows


def fetch_bloomberg_prices(canonical_ticker):
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]

    raw_data = fetch_raw_bloomberg_history(identifier)

    rows = normalize_bloomberg_history(
        raw_data,
        canonical_ticker,
    )

    if not rows:
        raise ValueError(f"No prices found for {canonical_ticker}")

    return rows
