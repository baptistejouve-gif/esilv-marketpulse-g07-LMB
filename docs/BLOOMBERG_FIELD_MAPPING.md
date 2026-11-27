# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

Source:
`data/sample/bloomberg_reference_sample.json`

Reference:
`docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md`

Live connectivity:
not demonstrated

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

> **Note:** The keys below (`observation_date`, `open_value`, etc.) are teaching wrapper keys from the approved fallback fixture (`teaching wrapper key != Bloomberg LIVE field mnemonic`).

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | Mapped to `YYYY-MM-DD` string |
| ticker | application mapping (`canonical_ticker`) | Preserved as `AAPL` or `SP500` (never provider ID) |
| open | `open_value` | Cast to `float` |
| high | `high_value` | Cast to `float` |
| low | `low_value` | Cast to `float` |
| close | `close_value` | Cast to `float` |
| volume | `volume_value` | Cast to `int` (`0` for `SPX Index` in sample) |

## TD10 handoff

- **Access mode:** `APPROVED_SAMPLE` (via `data/sample/bloomberg_reference_sample.json`)
- **Instrument identifier:** `AAPL US Equity` -> canonical `AAPL`
- **Benchmark identifier:** `SPX Index` -> canonical `SP500`
- **Date representation:** ISO string `YYYY-MM-DD` (`observation_date`)
- **Input structure:** JSON object containing a list of series, each with `provider_identifier`, `canonical_ticker`, and `observations` list
- **Missing fields:** None in the approved sample (`volume_value` is `0` for `SPX Index`, which is valid as an integer)
- **Special normalization notes:** Map `AAPL US Equity` -> `AAPL` and `SPX Index` -> `SP500` strictly inside `src/providers/bloomberg_provider.py` so `src/analytics.py` remains provider-neutral.
- **Expected canonical reference:** `data/sample/bloomberg_reference_expected.json`
