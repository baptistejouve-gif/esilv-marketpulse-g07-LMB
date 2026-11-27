from pathlib import Path
import json

ACCESS_MODE = "APPROVED_SAMPLE"
SAMPLE_PATH = Path("data/sample/bloomberg_reference_sample.json")

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

def fetch_raw_bloomberg_history(identifier, start_date=None, end_date=None, sample_path=SAMPLE_PATH):
    path = Path(sample_path)
    if not path.exists():
        raise FileNotFoundError(f"Approved sample file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, dict):
        if identifier in payload and isinstance(payload[identifier], list):
            return payload[identifier]
        for key in ("series", "data", "items", "records", "observations"):
            val = payload.get(key)
            if isinstance(val, dict) and identifier in val:
                return val[identifier]
            if isinstance(val, list):
                matched = [
                    row for row in val
                    if isinstance(row, dict) and row.get("provider_identifier") == identifier
                ]
                if matched:
                    if len(matched) == 1 and isinstance(matched[0].get("observations"), list):
                        return matched[0]["observations"]
                    return matched
    raise ValueError(f"No approved sample records found for identifier: {identifier}")

def normalize_bloomberg_history(raw_data, canonical_ticker):
    if not raw_data:
        raise ValueError(f"Empty Bloomberg-stage data for {canonical_ticker}")
    normalized = []
    for obs in raw_data:
        date_val = obs.get("observation_date", obs.get("date"))
        open_val = obs.get("open_value", obs.get("open"))
        high_val = obs.get("high_value", obs.get("high"))
        low_val = obs.get("low_value", obs.get("low"))
        close_val = obs.get("close_value", obs.get("close"))
        vol_val = obs.get("volume_value", obs.get("volume", 0))
        normalized.append({
            "date": str(date_val),
            "ticker": canonical_ticker,
            "open": float(open_val),
            "high": float(high_val),
            "low": float(low_val),
            "close": float(close_val),
            "volume": int(float(vol_val)),
        })
    return normalized

def get_bloomberg_series(canonical_ticker, sample_path=SAMPLE_PATH):
    if canonical_ticker not in BLOOMBERG_IDENTIFIERS:
        raise ValueError(f"Unsupported canonical ticker: {canonical_ticker}")
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_rows = fetch_raw_bloomberg_history(identifier, sample_path=sample_path)
    return normalize_bloomberg_history(raw_rows, canonical_ticker)
