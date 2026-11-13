import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    file_path = BASE_DIR / "data" / "sample" / "instruments.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    file_path = BASE_DIR / "data" / "sample" / "prices.csv"

    with open(file_path, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def get_prices_for_ticker(prices, ticker):
    return [
        price for price in prices
        if price["ticker"] == ticker
    ]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


# Maxandre's feature: validate market observations
def validate_prices(prices, ticker):
    if not prices:
        raise ValueError(f"No prices found for {ticker}")


def display_market_summary(instrument, prices, is_benchmark=False):
    ticker = instrument["ticker"]
    name = instrument["name"]

    print(f"{ticker} - {name}")
    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")

    if is_benchmark:
        print(f"First close  : {get_first_close(prices):.2f}")
        print(f"Last close   : {get_last_close(prices):.2f}")
    else:
        currency = instrument["currency"]
        print(f"First close  : {get_first_close(prices):.2f} {currency}")
        print(f"Last close   : {get_last_close(prices):.2f} {currency}")


def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = get_prices_for_ticker(
        prices, instrument["ticker"]
    )

    benchmark_prices = get_prices_for_ticker(
        prices, benchmark["ticker"]
    )

    # Validate the observations before using them
    validate_prices(instrument_prices, instrument["ticker"])
    validate_prices(benchmark_prices, benchmark["ticker"])

    print("=== MarketPulse ===")
    print()

    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print()

    print("Instrument")
    display_market_summary(instrument, instrument_prices)

    print()

    print("Benchmark")
    display_market_summary(
        benchmark,
        benchmark_prices,
        is_benchmark=True
    )


if __name__ == "__main__":
    main()