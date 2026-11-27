import json
from pathlib import Path

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

ACCESS_MODE = "APPROVED_SAMPLE"
SAMPLE_PATH = Path("data/sample/bloomberg_reference_sample.json")


def fetch_raw_bloomberg_history(identifier, start_date=None, end_date=None):
    """Load instructor-approved Bloomberg-stage sample input for the given identifier."""
    with open(SAMPLE_PATH, encoding="utf-8") as file:
        payload = json.load(file)

    for series in payload.get("series", []):
        if series.get("provider_identifier") == identifier:
            return series

    raise ValueError(f"Unsupported Bloomberg identifier in sample: {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    """Transform approved Bloomberg-stage series observations into MarketPulse canonical rows."""
    rows = []
    for observation in raw_data.get("observations", []):
        rows.append(
            {
                "date": observation["observation_date"],
                "ticker": canonical_ticker,
                "open": float(observation["open_value"]),
                "high": float(observation["high_value"]),
                "low": float(observation["low_value"]),
                "close": float(observation["close_value"]),
                "volume": int(observation["volume_value"]),
            }
        )
    return rows


def fetch_bloomberg_prices(canonical_ticker, start_date=None, end_date=None):
    """Fetch and normalize Bloomberg-stage prices for a canonical MarketPulse ticker."""
    if canonical_ticker not in BLOOMBERG_IDENTIFIERS:
        raise ValueError(f"Unsupported canonical ticker: {canonical_ticker}")

    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_series = fetch_raw_bloomberg_history(identifier, start_date=start_date, end_date=end_date)
    return normalize_bloomberg_history(raw_series, canonical_ticker)
