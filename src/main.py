import json
from pathlib import Path

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.bloomberg_provider import (
    ACCESS_MODE,
    BLOOMBERG_IDENTIFIERS,
    fetch_bloomberg_prices,
)

DATA_DIR = Path("data/sample")


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])


def build_market_snapshot(provider="bloomberg", lookback="1mo", interval="1d"):
    metadata = load_instruments()
    instrument = metadata["instrument"]
    benchmark = metadata["benchmark"]

    instrument_prices = fetch_bloomberg_prices(instrument["ticker"])
    benchmark_prices = fetch_bloomberg_prices(benchmark["ticker"])

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

    return {
        "provider": "Bloomberg stage",
        "access_mode": ACCESS_MODE,
        "provider_identifiers": BLOOMBERG_IDENTIFIERS,
        "lookback": lookback,
        "interval": interval,
        "instrument": instrument,
        "benchmark": benchmark,
        "aligned_instrument": aligned_instrument,
        "aligned_benchmark": aligned_benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
    }


def display_market_summary(asset, prices, period_return, show_currency=True):
    print(f"{asset['ticker']} - {asset['name']}")

    if "market" in asset:
        print(f"Market       : {asset['market']}")
    if "currency" in asset:
        print(f"Currency     : {asset['currency']}")

    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")
    print(f"First close  : {get_first_close(prices):.2f}")
    print(f"Last close   : {get_last_close(prices):.2f}")
    print(f"Period return: {period_return:+.2f}%\n")


def main():
    snapshot = build_market_snapshot()
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    aligned_instrument = snapshot["aligned_instrument"]
    aligned_benchmark = snapshot["aligned_benchmark"]

    print("MarketPulse - Market Summary\n")
    print(f"Provider     : {snapshot['provider']}")
    print(f"Access mode  : {snapshot['access_mode']}")
    print("Period       : 1 month")
    print("Interval     : Daily\n")

    print("Instrument")
    display_market_summary(
        instrument,
        aligned_instrument,
        snapshot["instrument_return"],
        show_currency=True,
    )

    print("Benchmark")
    display_market_summary(
        benchmark,
        aligned_benchmark,
        snapshot["benchmark_return"],
        show_currency=False,
    )

    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{snapshot['relative_performance']:+.2f} percentage points\n"
    )

    print("Base 100")
    print(
        f"{instrument['ticker']:<5} : "
        f"{snapshot['instrument_base_100'][0]['value']:.2f} -> "
        f"{snapshot['instrument_base_100'][-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']:<5} : "
        f"{snapshot['benchmark_base_100'][0]['value']:.2f} -> "
        f"{snapshot['benchmark_base_100'][-1]['value']:.2f}"
    )


if __name__ == "__main__":
    main()
