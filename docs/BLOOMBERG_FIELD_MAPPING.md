

\# Bloomberg Field Mapping



\## Access mode



APPROVED\_SAMPLE



\- Source: `data/sample/bloomberg\_reference\_sample.json`

\- Expected canonical reference: `data/sample/bloomberg\_reference\_expected.json`

\- Instructor reference: `docs/10\_BLOOMBERG\_INSTRUCTOR\_REFERENCE.md`

\- Live connectivity: not demonstrated.



The instructor reference document was not available

in the local repository at the time of inspection.

The mapping below is based on the supplied JSON fixtures

and the TD09 instructions.



The sample contains illustrative teaching values reused

from the local CSV dataset. These are not certified

Bloomberg historical observations.



\## Market instruments



| Role | Canonical ticker | Bloomberg identifier |

|---|---|---|

| Instrument | AAPL | AAPL US Equity |

| Benchmark | SP500 | SPX Index |



\## Input inspection



\### Instrument



\- Canonical ticker: AAPL

\- Provider identifier: AAPL US Equity

\- Observations: 21

\- First date: 2026-09-01

\- Last date: 2026-09-30

\- First close: 250.00

\- Last close: 266.20

\- Missing fields: none observed.



\### Benchmark



\- Canonical ticker: SP500

\- Provider identifier: SPX Index

\- Observations: 21

\- First date: 2026-09-01

\- Last date: 2026-09-30

\- First close: 6600.00

\- Last close: 6742.00

\- Missing fields: none observed.

\- Volume: zero in all sample observations.



\## Input structure



The JSON fixture contains a list named `series`.



Each series contains:



\- role

\- canonical\_ticker

\- provider\_identifier

\- observations



Each observation contains a date and six-field

market data structure, including OHLC and volume

(five numeric fields and one date field).



\## Field mapping



| MarketPulse field | Source field or mapping | Status / notes |

|---|---|---|

| date | observation\_date | String, YYYY-MM-DD |

| ticker | canonical\_ticker | AAPL or SP500, inherited from the parent series |

| open | open\_value | Convert to float |

| high | high\_value | Convert to float |

| low | low\_value | Convert to float |

| close | close\_value | Convert to float |

| volume | volume\_value | Convert to int |



The source fields are teaching wrapper keys,

not Bloomberg LIVE field mnemonics.



No unverified Bloomberg field mnemonic is assumed.



\## Expected canonical rows



Example instrument row:



```json

{

&#x20;   "date": "2026-09-01",

&#x20;   "ticker": "AAPL",

&#x20;   "open": 249.2,

&#x20;   "high": 251.5,

&#x20;   "low": 248.0,

&#x20;   "close": 250.0,

&#x20;   "volume": 38000000

}

```



Example benchmark row:



```json

{

&#x20;   "date": "2026-09-01",

&#x20;   "ticker": "SP500",

&#x20;   "open": 6592.0,

&#x20;   "high": 6615.0,

&#x20;   "low": 6580.0,

&#x20;   "close": 6600.0,

&#x20;   "volume": 0

}

```



\## TD10 handoff



\- Access mode: APPROVED\_SAMPLE.

\- Instrument identifier: AAPL US Equity.

\- Benchmark identifier: SPX Index.

\- Date representation: YYYY-MM-DD.

\- Input structure: JSON containing two series.

\- Missing fields: none observed in the sample.

\- Expected canonical reference:

&#x20; `data/sample/bloomberg\_reference\_expected.json`.

\- Preserve AAPL and SP500 as canonical tickers.

\- Convert OHLC values to floats and volume to integers.

\- Preserve the benchmark volume provided by the fixture.

\- Reuse the existing common-date alignment.

\- Reuse TD07 analytics without provider-specific changes.

\- Keep Bloomberg identifiers at the provider boundary.

\- Do not present sample data as LIVE Bloomberg data.



\## Conclusion



The Bloomberg-stage sample can be mapped to the

existing MarketPulse canonical row structure.



The TD10 provider should implement this normalization

while preserving the existing analytics layer.



Live Bloomberg connectivity has not been demonstrated.



