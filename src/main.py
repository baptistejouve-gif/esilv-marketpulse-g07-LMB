from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.bloomberg_provider import ACCESS_MODE, get_bloomberg_series

def build_market_snapshot(provider="bloomberg", lookback="1mo", interval="1d"):
    instrument_rows = get_bloomberg_series("AAPL")
    benchmark_rows = get_bloomberg_series("SP500")
    aligned_instrument, aligned_benchmark = align_series(instrument_rows, benchmark_rows)
    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(instrument_return, benchmark_return)
    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)
    return {
        "provider": provider,
        "access_mode": ACCESS_MODE,
        "lookback": lookback,
        "interval": interval,
        "instrument": "AAPL - Apple Inc.",
        "benchmark": "S&P 500",
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
    }

def _extract_metric(val):
    if isinstance(val, dict):
        for k in ("return", "period_return", "value"):
            if k in val:
                return float(val[k])
        return float(next(iter(val.values())))
    return float(val)

def _extract_base100_last(series):
    last = series[-1]
    if isinstance(last, dict):
        for k in ("base_100", "base100", "value"):
            if k in last:
                return float(last[k])
        return float(list(last.values())[-1])
    return float(last)

def main():
    snapshot = build_market_snapshot()
    inst_ret = _extract_metric(snapshot["instrument_return"]) * 100
    bench_ret = _extract_metric(snapshot["benchmark_return"]) * 100
    rel_perf = _extract_metric(snapshot["relative_performance"]) * 100
    inst_b100 = _extract_base100_last(snapshot["instrument_base_100"])
    bench_b100 = _extract_base100_last(snapshot["benchmark_base_100"])
    print("Provider")
    print("Bloomberg stage")
    print("")
    print("Access mode")
    print(snapshot["access_mode"])
    print("")
    print("Market configuration")
    print(f"Instrument : {snapshot["instrument"]}")
    print(f"Benchmark  : {snapshot["benchmark"]}")
    print("Period     : 1 month")
    print("Interval   : Daily")
    print("")
    print(f"Instrument return   : {inst_ret:+.2f}%")
    print(f"Benchmark return    : {bench_ret:+.2f}%")
    print(f"Relative performance: {rel_perf:+.2f} percentage points")
    print(f"Base 100 final      : AAPL {inst_b100:.2f} | SP500 {bench_b100:.2f}")

if __name__ == "__main__":
    main()
