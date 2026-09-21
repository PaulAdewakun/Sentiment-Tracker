# Sentiment-Driven Energy Signal Engine
**Sector-Focused Sentiment & Price Lag-Correlation Study**

## Overview

This project investigates a real, testable question: does news and social sentiment *lead* stock price movement, *lag* it, or show no reliable relationship at all — for a curated basket of GICS Energy-sector equities? Rather than building a generic sentiment dashboard, the goal is to answer that question directly, using lag-correlation analysis across multiple time horizons (1, 3, and 5 trading days).

## Status

- ✅ **Phase 1 — Data Pipeline (Complete):** Automated pipeline pulls and stores full daily split/dividend-adjusted OHLCV price history for the ticker basket into a local SQLite database.
- 🔲 **Phase 2 — Sentiment Scoring (Planned):** A dual-source sentiment layer — Alpha Vantage's News & Sentiment API, cross-validated against an independent VADER NLP pass over the same headlines — to catch unreliable readings before they feed the analysis.
- 🔲 **Phase 3 — Lag-Correlation Analysis (Planned):** Test whether sentiment shifts lead or lag forward stock returns at 1-, 3-, and 5-day horizons using pandas and NumPy, visualized in Matplotlib.
- 🔲 **Phase 4 — Dashboard (Stretch Goal):** Optional Streamlit interface for exploring results interactively.

## Ticker Basket

| Ticker | Company |
|--------|---------|
| SU | Suncor Energy |
| CNQ | Canadian Natural Resources |
| IMO | Imperial Oil |
| SLB | SLB (Schlumberger) |
| XOM | ExxonMobil |

The basket is scoped specifically to companies classified under **GICS Energy** — not Utilities. This distinction matters: electric utilities that happen to operate nuclear plants (e.g. Constellation Energy, Vistra) are classified under GICS *Utilities* despite the sector-adjacent branding, so names like those were deliberately left out to keep the basket sector-consistent.

## How It Works

1. `Main.py` loops through the ticker basket and pulls full daily-adjusted price history for each symbol via `yfinance`.
2. Data is written to a local SQLite database (`financialData.db`), in a `daily_adjusted_prices` table.
3. A composite primary key on `(ticker, date)` makes reruns idempotent — `INSERT OR REPLACE` lets the script run again to pick up new trading days without creating duplicates, and automatically overwrites historical rows if a retroactive dividend or split changes past adjusted values.

## Getting Started

```bash
pip install yfinance
python Main.py
```

No API key is required for this stage. Running the script pulls and stores full-history OHLCV data (open, high, low, close, adjusted close, volume, dividends, and split events) for all five tickers.

## Tech Stack

**In use:**
- Python
- `yfinance` — price data
- `sqlite3` — local storage

**Planned for later phases:**
- Alpha Vantage API — News & Sentiment
- `vaderSentiment` (VADER) — independent NLP sentiment scoring
- pandas, NumPy — lag-correlation analysis
- Matplotlib — visualization

## Known Limitations & Design Decisions

- **Alpha Vantage's free tier changed twice during development**, and price data was moved off it as a result. It originally supplied price data via `TIME_SERIES_DAILY_ADJUSTED`, but Alpha Vantage moved that endpoint behind a paid plan. Switching to the free `TIME_SERIES_DAILY` endpoint ran into a second restriction: `outputsize=full` (multi-year history) is now premium-only across all of Alpha Vantage's daily endpoints, capping free access at the most recent 100 data points — too little history for a meaningful lag-correlation study. Price data was moved to `yfinance` instead, which is free, has no daily request cap, and still provides split/dividend-adjusted close prices.
- Alpha Vantage remains the planned source for the sentiment side of the project, since its News & Sentiment endpoint hasn't shown the same restriction.
- Without a completed sentiment layer yet, no findings are reported here — this section will be updated once Phase 2 and 3 are complete.

## Project Structure

```
Database/
├── Main.py           # Price data pipeline (yfinance → SQLite)
├── financialData.db  # SQLite database (created on first run)
└── README.md
```

## Future Work / Stretch Goals

- Complete the dual-source sentiment-scoring layer
- Run the 1/3/5-day lag-correlation analysis and report an actual finding
- Contrarian filter — flag days where sentiment and price diverge sharply
- Time-decay weighting so recent sentiment counts more than older posts
- A second sector added for comparison, to test whether any sentiment/price relationship is sector-specific
- Backtest a simple sentiment-based trading rule
- Public dashboard deployment
