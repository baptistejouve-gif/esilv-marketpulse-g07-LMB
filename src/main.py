import csv
import json
from pathlib import Path

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)

DATA_DIR = Path("data/sample")


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


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])


def display_market_summary(asset, prices, period_return, show_currency=True):
    print(f"{asset['ticker']} - {asset['name']}")

    if "market" in asset:
        print(f"Market        : {asset['market']}")
    if "currency" in asset:
        print(f"Currency      : {asset['currency']}")

    print(f"Observations  : {len(prices)}")
    print(f"First date    : {get_first_date(prices)}")
    print(f"Last date     : {get_last_date(prices)}")

    currency_str = f" {asset.get('currency', '')}" if show_currency else ""
    print(f"First close   : {get_first_close(prices):.2f}{currency_str}")
    print(f"Last close    : {get_last_close(prices):.2f}{currency_str}")
    print(f"Period return : {period_return:+.2f}%\n")


def main():
    print("=== MarketPulse ===\n")

    instruments = load_instruments()
    raw_prices = load_prices()
    normalized_prices = [normalize_price_row(row) for row in raw_prices]

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(normalized_prices, instrument["ticker"])
    benchmark_prices = filter_prices(normalized_prices, benchmark["ticker"])

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    print("Market configuration")
    print("Period   : 1 month")
    print("Interval : Daily\n")

    print("Instrument")
    display_market_summary(
        instrument,
        aligned_instrument,
        instrument_return,
        show_currency=True,
    )

    print("Benchmark")
    display_market_summary(
        benchmark,
        aligned_benchmark,
        benchmark_return,
        show_currency=False,
    )

    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{relative_performance:+.2f} percentage points\n"
    )

    print("Base 100")
    print(
        f"{instrument['ticker']:<5} : "
        f"{instrument_base_100[0]['value']:.2f} -> "
        f"{instrument_base_100[-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']:<5} : "
        f"{benchmark_base_100[0]['value']:.2f} -> "
        f"{benchmark_base_100[-1]['value']:.2f}"
    )


if __name__ == "__main__":
    main()
