
from pathlib import Path
import json

from providers.yahoo_provider import (
    fetch_yahoo_prices,
    YAHOO_SYMBOLS,
)

from analytics import (
    align_series,
    calculate_period_return,
    calculate_relative_performance,
    calculate_base_100,
)

DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"

PERIOD = "1mo"
INTERVAL = "1d"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def validate_prices(prices, ticker):
    if not prices:
        raise ValueError(f"No prices found for {ticker}")


def display_market_summary(asset, prices, show_currency=True):
    print(f"{asset['ticker']} - {asset['name']}")

    if "market" in asset:
        print(f"Market       : {asset['market']}")

    if "currency" in asset:
        print(f"Currency     : {asset['currency']}")

    print(f"Observations : {len(prices)}")

    first_date = prices[0]["date"]
    last_date = prices[-1]["date"]
    first_close = prices[0]["close"]
    last_close = prices[-1]["close"]

    currency_str = (
        f" {asset.get('currency', '')}"
        if show_currency else ""
    )

    print(f"First date   : {first_date}")
    print(f"Last date    : {last_date}")
    print(f"First close  : {first_close:.2f}{currency_str}")
    print(f"Last close   : {last_close:.2f}{currency_str}")


def main():
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    # Retrieve remote Yahoo Finance data
    instrument_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[instrument["ticker"]],
        canonical_ticker=instrument["ticker"],
        period=PERIOD,
        interval=INTERVAL,
    )

    benchmark_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[benchmark["ticker"]],
        canonical_ticker=benchmark["ticker"],
        period=PERIOD,
        interval=INTERVAL,
    )

    validate_prices(instrument_prices, instrument["ticker"])
    validate_prices(benchmark_prices, benchmark["ticker"])

    # Align observations on common dates
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument or not aligned_benchmark:
        raise ValueError("No common observation dates")

    # Reuse TD07 analytics
    instrument_return = calculate_period_return(
        aligned_instrument
    )

    benchmark_return = calculate_period_return(
        aligned_benchmark
    )

    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base_100 = calculate_base_100(
        aligned_instrument
    )

    benchmark_base_100 = calculate_base_100(
        aligned_benchmark
    )

    print("=== MarketPulse ===")
    print()

    print("Provider")
    print("Yahoo Finance via yfinance")
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
