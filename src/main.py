
from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_period_return,
    calculate_relative_performance,
    calculate_base_100,
)

DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def validate_prices(prices, ticker):
    if not prices:
        raise ValueError(f"No prices found for {ticker}")


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def get_first_close(prices):
    return prices[0]["close"]


def get_last_close(prices):
    return prices[-1]["close"]


def display_market_summary(asset, prices, show_currency=True):
    print(f"{asset['ticker']} - {asset['name']}")

    if "market" in asset:
        print(f"Market       : {asset['market']}")

    if "currency" in asset:
        print(f"Currency     : {asset['currency']}")

    print(f"Observations : {len(prices)}")

    first_date = get_first_date(prices)
    last_date = get_last_date(prices)
    first_close = get_first_close(prices)
    last_close = get_last_close(prices)

    currency_str = f" {asset.get('currency', '')}" if show_currency else ""

    print(f"First date   : {first_date}")
    print(f"Last date    : {last_date}")
    print(f"First close  : {first_close:.2f}{currency_str}")
    print(f"Last close   : {last_close:.2f}{currency_str}")


def main():
    instruments = load_instruments()
    prices = load_prices()

    normalized_prices = [
        normalize_price_row(row)
        for row in prices
    ]

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(
        normalized_prices, instrument["ticker"]
    )

    benchmark_prices = filter_prices(
        normalized_prices, benchmark["ticker"]
    )

    validate_prices(instrument_prices, instrument["ticker"])
    validate_prices(benchmark_prices, benchmark["ticker"])

    # Align both series on common dates
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument or not aligned_benchmark:
        raise ValueError("No common observation dates")

    # Calculate period returns
    instrument_return = calculate_period_return(
        aligned_instrument
    )

    benchmark_return = calculate_period_return(
        aligned_benchmark
    )

    # Calculate relative performance
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    # Calculate base-100 series
    instrument_base_100 = calculate_base_100(
        aligned_instrument
    )

    benchmark_base_100 = calculate_base_100(
        aligned_benchmark
    )

    print("=== MarketPulse ===")
    print()

    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print()

    print("Instrument")
    display_market_summary(instrument, aligned_instrument)
    print(f"Period return : {instrument_return:.2f}%")
    print()

    print("Benchmark")
    display_market_summary(benchmark, aligned_benchmark, False)
    print(f"Period return : {benchmark_return:.2f}%")
    print()

    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{relative_performance:+.2f} percentage points"
    )
    print()

    print("Base 100")

    print(
        f"{instrument['ticker']} : "
        f"{instrument_base_100[0]['value']:.2f} -> "
        f"{instrument_base_100[-1]['value']:.2f}"
    )

    print(
        f"{benchmark['ticker']} : "
        f"{benchmark_base_100[0]['value']:.2f} -> "
        f"{benchmark_base_100[-1]['value']:.2f}"
    )


if __name__ == "__main__":
    main()
