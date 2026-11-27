
from pathlib import Path
import json

if __package__:
    from .providers.bloomberg_provider import (
        fetch_bloomberg_prices,
        ACCESS_MODE,
    )
    from .analytics import (
        align_series,
        calculate_period_return,
        calculate_relative_performance,
        calculate_base_100,
    )
else:
    from providers.bloomberg_provider import (
        fetch_bloomberg_prices,
        ACCESS_MODE,
    )
    from analytics import (
        align_series,
        calculate_period_return,
        calculate_relative_performance,
        calculate_base_100,
    )


DATA_DIR = Path(__file__).resolve().parents[1] / "data/sample"

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def build_market_snapshot():
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = fetch_bloomberg_prices(
        instrument["ticker"]
    )

    benchmark_prices = fetch_bloomberg_prices(
        benchmark["ticker"]
    )

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument or not aligned_benchmark:
        raise ValueError("No common observation dates")

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

    return {
        "provider": "Bloomberg stage",
        "access_mode": ACCESS_MODE,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_prices": aligned_instrument,
        "benchmark_prices": aligned_benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
    }


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
    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]

    print("=== MarketPulse ===")
    print()

    print("Provider")
    print(snapshot["provider"])
    print()

    print("Access mode")
    print(snapshot["access_mode"])
    print()

    print("Market configuration")
    print(f"Period   : {snapshot['lookback']}")
    print(f"Interval : {snapshot['interval']}")
    print()

    print("Instrument")

    display_market_summary(
        instrument,
        snapshot["instrument_prices"],
    )

    print(f"Period return : {snapshot['instrument_return']:.2f}%")
    print()

    print("Benchmark")

    display_market_summary(
        benchmark,
        snapshot["benchmark_prices"],
        False,
    )

    print(f"Period return : {snapshot['benchmark_return']:.2f}%")
    print()

    print("Relative performance")

    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{snapshot['relative_performance']:+.2f} percentage points"
    )

    print()
    print("Base 100")

    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

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
