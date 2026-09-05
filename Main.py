# Below are the import statements for the necessary libraries. Make sure to install the required packages using pip if you haven't already.
from alpha_vantage.timeseries import TimeSeries
import time
import os
import sqlite3

# Establishing the API key for Alpha Vantage. Make sure to set your environment variable ALPHA_VANTAGE_API_KEY before running the script.
API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")  # Load your API key from an environment variable for security

# Error check to ensure the API key is present
if not API_KEY:
    raise ValueError("API key not found. Please set the ALPHA_VANTAGE_API_KEY environment variable.")

# Currated basket of energy stock tickers in the GICS Sector
TICKERS = ['SU','CNQ','IMO','SLB','XOM']

# A time delay of 15 seconds between API calls is set to comply with ALPHA VANTAGE's free tier limit of 5 calls/minute. 
# This buffer was chosen as it offers a safe margin to avoid hitting the rate limit while accounting for any delays in response time from the API.
SECONDS_BETWEEN_CALLS = 15

# Creating a timeseries object, api key loaded in below
ts = TimeSeries(key=API_KEY, output_format='json')

# Function to create a SQLite database connection
def create_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_adjusted_prices(
        ticker              TEXT NOT NULL,
        date                TEXT NOT NULL,
        open                REAL,
        close               REAL,
        adjusted_close      REAL,
        volume              INTEGER,
        dividend_amount     REAL,
        split_coefficient   REAL,
        PRIMARY KEY(ticker, date)
        )
        """
    )
    conn.commit()

def insert_ticker_data(conn, ticker, daily_data):
    rows = []

    for date, value in daily_data.item():
        rows.append((
            ticker,
            date,
            float(value.get("1. open")),
            float(value.get("2. high")),
            float(value.get("3. low")),
            float(value.get("4. close")),
            float(value.get("5. adjusted close")),
            float(value.get("6. volume")),
            float(value.get("7. dividend amount")),
            float(value.get("8. split coefficient")),
        ))
    conn.executemany("""
    INSERT OR REPLACE INTO daily_adjusted_prices
    (ticker, date, open, high, low, close, adjusted close, volume, dividend amount, split coefficient)
    VALUES (?,?,?,?,?,?,?,?,?,?)
    """, rows)
    conn.commit()
    return len(rows)

def main():
    con = sqlite3.connect("financialData.db")
    create_table(con)

    for i, ticker in enumerate(TICKERS):
        print(f"Pulling {ticker} ({i+1}/{len(TICKERS)})...")

        try:
            daily_data,_= ts.get_daily_adjusted(symbol=ticker, output='full')

        except Exception as e:
            print(f"Failed to pull {ticker}: {e}")

        row_count = insert_ticker_data(con, ticker, daily_data)
        print(f"Stored {row_count} rows for {ticker} in financialData.db")

        if i < len(TICKERS)-1:
            time.sleep(SECONDS_BETWEEN_CALLS)

    con.close()
    print("\nnDone pulling all data.")

if __name__ == main:
    main()
