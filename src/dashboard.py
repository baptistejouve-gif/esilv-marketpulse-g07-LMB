
from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot


# Load the shared MarketPulse snapshot
snapshot = build_market_snapshot()

provider = snapshot["provider"]
access_mode = snapshot.get("access_mode", "")
lookback = snapshot["lookback"]
interval = snapshot["interval"]

instrument = snapshot["instrument"]
benchmark = snapshot["benchmark"]

instrument_return = snapshot["instrument_return"]
benchmark_return = snapshot["benchmark_return"]
relative_performance = snapshot["relative_performance"]

instrument_base_100 = snapshot["instrument_base_100"]
benchmark_base_100 = snapshot["benchmark_base_100"]


# Initialize Dash
app = Dash(__name__)
app.title = "MarketPulse | Market Analytics"


# Dashboard colors
BACKGROUND = "#0B1120"
CARD = "#151E2E"
BORDER = "#263449"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"
BLUE = "#38BDF8"
ORANGE = "#F59E0B"
GREEN = "#22C55E"
RED = "#EF4444"


# Shared card style
card_style = {
    "backgroundColor": CARD,
    "border": f"1px solid {BORDER}",
    "borderRadius": "12px",
    "padding": "20px",
    "flex": "1",
}


def performance_card(title, value, unit):
    color = GREEN if value >= 0 else RED

    return html.Div(
        [
            html.Div(
                title,
                style={
                    "color": MUTED,
                    "fontSize": "14px",
                },
            ),
            html.Div(
                f"{value:+.2f}{unit}",
                style={
                    "color": color,
                    "fontSize": "34px",
                    "fontWeight": "bold",
                    "marginTop": "12px",
                },
            ),
        ],
        style=card_style,
    )


# Market configuration
context = html.Div(
    [
        html.H3("Market Configuration"),

        html.P(f"Provider: {provider}"),
        html.P(f"Access mode: {access_mode}"),

        html.P(
            f"Instrument: {instrument['ticker']} - "
            f"{instrument['name']}"
        ),

        html.P(
            f"Benchmark: {benchmark['ticker']} - "
            f"{benchmark['name']}"
        ),

        html.P(f"Lookback: {lookback}"),
        html.P(f"Interval: {interval}"),
    ],
    style={
        **card_style,
        "marginBottom": "20px",
        "lineHeight": "1.5",
    },
)


# Performance indicators
performance = html.Div(
    [
        performance_card(
            f"{instrument['ticker']} Return",
            instrument_return,
            "%",
        ),

        performance_card(
            f"{benchmark['ticker']} Return",
            benchmark_return,
            "%",
        ),

        performance_card(
            "Relative Performance",
            relative_performance,
            " pts",
        ),
    ],
    style={
        "display": "flex",
        "gap": "20px",
        "flexWrap": "wrap",
        "marginBottom": "20px",
    },
)


# Base-100 comparison chart
figure = go.Figure()

figure.add_trace(
    go.Scatter(
        x=[row["date"] for row in instrument_base_100],
        y=[row["value"] for row in instrument_base_100],
        mode="lines",
        name=instrument["ticker"],
        line={"color": BLUE, "width": 3},
        hovertemplate="%{x}<br>Base 100: %{y:.2f}<extra></extra>",
    )
)

figure.add_trace(
    go.Scatter(
        x=[row["date"] for row in benchmark_base_100],
        y=[row["value"] for row in benchmark_base_100],
        mode="lines",
        name=benchmark["ticker"],
        line={"color": ORANGE, "width": 3},
        hovertemplate="%{x}<br>Base 100: %{y:.2f}<extra></extra>",
    )
)

figure.add_hline(
    y=100,
    line_dash="dot",
    line_color=MUTED,
)

figure.update_layout(
    title="Instrument vs Benchmark - Base 100",
    xaxis_title="Date",
    yaxis_title="Base 100",
    template="plotly_dark",
    paper_bgcolor=CARD,
    plot_bgcolor=CARD,
    font={"color": TEXT},
    hovermode="x unified",
    height=450,
    legend={
        "orientation": "h",
        "y": 1.02,
        "x": 1,
        "xanchor": "right",
    },
    margin={"l": 60, "r": 30, "t": 80, "b": 60},
)

figure.update_xaxes(gridcolor=BORDER)
figure.update_yaxes(gridcolor=BORDER)


# Final dashboard layout
app.layout = html.Div(
    [
        html.H1(
            "MarketPulse",
            style={
                "fontSize": "38px",
                "marginBottom": "5px",
                "color": BLUE,
            },
        ),

        html.P(
            "Financial Market Analytics | Instrument vs Benchmark",
            style={
                "color": MUTED,
                "marginBottom": "30px",
            },
        ),

        context,

        performance,

        html.Div(
            [
                dcc.Graph(
                    figure=figure,
                    config={"displaylogo": False},
                )
            ],
            style=card_style,
        ),

        html.P(
            f"Data source: {provider} | {access_mode} | "
            "MarketPulse - ESILV",
            style={
                "color": MUTED,
                "textAlign": "center",
                "fontSize": "12px",
                "marginTop": "25px",
            },
        ),
    ],
    style={
        "backgroundColor": BACKGROUND,
        "color": TEXT,
        "minHeight": "100vh",
        "fontFamily": "Arial, sans-serif",
        "padding": "30px",
        "boxSizing": "border-box",
    },
)


if __name__ == "__main__":
    app.run(debug=False)
=======
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
