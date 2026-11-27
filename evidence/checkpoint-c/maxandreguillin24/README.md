# Checkpoint C Evidence - Maxandre Guillin (`maxandreguillin24`)

- **Repository:** `esilv-marketpulse-g07-LMB`
- **Final Authorized Provider & Mode:** `Bloomberg stage - APPROVED_SAMPLE` (`data/sample/bloomberg_reference_sample.json`)
- **Instrument vs Benchmark:** `AAPL` (Apple Inc.) vs `SP500` (S&P 500)
- **Lookback / Interval:** `1 month` / `Daily`

## Personal Contributions (TD09 - TD12)

- **TD09:** Canonical mapping and Bloomberg boundary preparation.
- **TD10:** Bloomberg provider boundary implementation and snapshot validation (`APPROVED_SAMPLE`).
- **TD11:** Dash visual dashboard consuming `build_market_snapshot()` (`src/dashboard.py`, `requirements.txt`).
- **TD12:** Final release documentation (`README.md`), clean reproducibility test, and PR #32 integration into `main`.

## Commands Executed

- `python3 -m pip install -r requirements.txt`
- `python3 src/main.py`
- `python3 src/dashboard.py`
