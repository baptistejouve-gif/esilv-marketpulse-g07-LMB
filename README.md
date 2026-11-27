# MarketPulse

MarketPulse compares a primary financial instrument (`AAPL`) against a market benchmark (`SP500`) over a 1-month daily window using canonical OHLCV rows, shared analytics (`align_series`, period return, Base 100, relative performance), a shared application snapshot (`build_market_snapshot`), a terminal report, and a static Dash dashboard.

## Market Configuration

- **Instrument:** `AAPL` — Apple Inc. (`AAPL US Equity`)
- **Benchmark:** `SP500` — S&P 500 (`SPX Index`)
- **Lookback:** `1mo` (1 month)
- **Interval:** `1d` (Daily)
- **Provider & Access Mode:** `Bloomberg stage - APPROVED_SAMPLE` (using approved fallback fixture `data/sample/bloomberg_reference_sample.json`; live Bloomberg connectivity not demonstrated)

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run Terminal Path

```bash
python src/main.py
```

## Run Dashboard Path

```bash
python src/dashboard.py
```

Open the local URL displayed by Dash (`http://127.0.0.1:8050/`) to view the comparison context, return metrics, and Base-100 chart.

## Environment Constraints & Evidence

- Bloomberg terminal live connectivity is not available in this Codespace environment; normalization follows the approved sample contract documented in `docs/BLOOMBERG_FIELD_MAPPING.md`.
- Checkpoint C evidence files (`README.md`, `01_final_market_data.png`, `02_dash_dashboard.png`, `03_final_pull_request.png`, `04_reproducible_run.png`) are stored under `evidence/checkpoint-c/<github-username>/` per `docs/04_CHECKPOINTS_AND_EVIDENCE.md`.
