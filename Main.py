"""
Pull daily adjusted price data for a curated basket of tickers using yfinance,
and store it in a local SQLite database.

Note: yfinance returns data as a pandas DataFrame internally — that's just how
the library works, and unavoidable. This script still converts it to plain
tuples before writing, so the actual database step stays pure sqlite3.

Usage:
    pip install yfinance
    python Main.py
"""

import time
import sqlite3
import yfinance as yf

# Curated basket of energy stock tickers in the GICS Energy sector
TICKERS = ['SU', 'CNQ', 'IMO', 'SLB', 'XOM']

# yfinance has no official rate limit like Alpha Vantage, but a short pause
# between tickers is good practice to avoid being throttled for bulk requests.
SECONDS_BETWEEN_CALLS = 2


def create_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_adjusted_prices (
            ticker             TEXT    NOT NULL,
            date               TEXT    NOT NULL,
            open               REAL,
            high               REAL,
            low                REAL,
            close              REAL,
            adjusted_close     REAL,
            volume             INTEGER,
            dividend_amount    REAL,
            split_coefficient  REAL,
            PRIMARY KEY (ticker, date)
        )
        """
    )
    conn.commit()


def insert_ticker_data(conn, ticker, history_df):
    rows = []

    for date, row in history_df.iterrows():
        # yfinance uses 0 to mean "no split that day"; our schema (matching
        # Alpha Vantage's convention) uses 1.0 to mean the same thing.
        split_value = float(row["Stock Splits"]) if row["Stock Splits"] != 0 else 1.0

        rows.append((
            ticker,
            date.strftime("%Y-%m-%d"),
            float(row["Open"]),
            float(row["High"]),
            float(row["Low"]),
            float(row["Close"]),
            float(row["Adj Close"]),
            int(row["Volume"]),
            float(row["Dividends"]),
            split_value,
        ))

    conn.executemany(
        """
        INSERT OR REPLACE INTO daily_adjusted_prices
            (ticker, date, open, high, low, close, adjusted_close,
             volume, dividend_amount, split_coefficient)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    return len(rows)


def main():
    con = sqlite3.connect("financialData.db")
    create_table(con)

    for i, ticker in enumerate(TICKERS):
        print(f"Pulling {ticker} ({i + 1}/{len(TICKERS)})...")

        try:
            history_df = yf.Ticker(ticker).history(
                period="max", auto_adjust=False, actions=True
            )
            if history_df.empty:
                raise ValueError("No data returned")
        except Exception as e:
            print(f"Failed to pull {ticker}: {e}")
            continue

        row_count = insert_ticker_data(con, ticker, history_df)
        print(f"Stored {row_count} rows for {ticker} in financialData.db")

        if i < len(TICKERS) - 1:
            time.sleep(SECONDS_BETWEEN_CALLS)

    con.close()
    print("\nDone pulling all data.")


if __name__ == "__main__":
    main()