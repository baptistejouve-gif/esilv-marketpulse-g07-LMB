from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot

def _metric_num(val):
    if isinstance(val, dict):
        for k in ("return", "period_return", "value"):
            if k in val:
                return float(val[k])
        return float(next(iter(val.values())))
    return float(val)

def _series_xy(series):
    xs, ys = [], []
    for item in series:
        if isinstance(item, dict):
            d = item.get("date", item.get("observation_date", ""))
            v = item.get("value", item.get("base_100", item.get("base100", item.get("close"))))
            xs.append(d)
            ys.append(float(v))
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            xs.append(item[0])
            ys.append(float(item[1]))
    return xs, ys

app = Dash(__name__)
snapshot = build_market_snapshot()

provider_label = f"{snapshot.get("provider", "bloomberg")} ({snapshot.get("access_mode", "APPROVED_SAMPLE")})"
lookback = snapshot.get("lookback", "1mo")
interval = snapshot.get("interval", "1d")
instrument = snapshot.get("instrument", "AAPL - Apple Inc.")
benchmark = snapshot.get("benchmark", "S&P 500")

inst_name = f"{instrument.get("ticker", "")} - {instrument.get("name", "")}".strip(" -") if isinstance(instrument, dict) else str(instrument)
bench_name = f"{benchmark.get("ticker", "")} - {benchmark.get("name", "")}".strip(" -") if isinstance(benchmark, dict) else str(benchmark)
inst_legend = instrument.get("ticker", "AAPL") if isinstance(instrument, dict) else "AAPL"
bench_legend = benchmark.get("ticker", "SP500") if isinstance(benchmark, dict) else "SP500"

inst_ret = _metric_num(snapshot["instrument_return"]) * 100
bench_ret = _metric_num(snapshot["benchmark_return"]) * 100
rel_perf = _metric_num(snapshot["relative_performance"]) * 100

inst_x, inst_y = _series_xy(snapshot["instrument_base_100"])
bench_x, bench_y = _series_xy(snapshot["benchmark_base_100"])

figure = go.Figure()
figure.add_trace(go.Scatter(x=inst_x, y=inst_y, mode="lines", name=inst_legend))
figure.add_trace(go.Scatter(x=bench_x, y=bench_y, mode="lines", name=bench_legend))
figure.update_layout(
    title="Instrument vs Benchmark - Base 100",
    xaxis_title="Date",
    yaxis_title="Base 100",
)

context = html.Div([
    html.P(f"Provider: {provider_label}"),
    html.P(f"Instrument: {inst_name}"),
    html.P(f"Benchmark: {bench_name}"),
    html.P(f"Lookback: {lookback}"),
    html.P(f"Interval: {interval}"),
])

performance = html.Div([
    html.Div([html.H3("Instrument Return"), html.P(f"{inst_ret:+.2f}%")]),
    html.Div([html.H3("Benchmark Return"), html.P(f"{bench_ret:+.2f}%")]),
    html.Div([html.H3("Relative Performance"), html.P(f"{rel_perf:+.2f} pts")]),
])

app.layout = html.Div([
    html.H1("MarketPulse"),
    context,
    performance,
    dcc.Graph(figure=figure),
])

if __name__ == "__main__":
    app.run(debug=False)
