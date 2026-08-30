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
def Create_Table(conn):
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


"""
# historical_data = historical price data, ts.get_daily_adjusted returns a tuple with the first element being the data and the second being metadata
# meta_data = metadata about the data, such as the last refreshed date and the interval of the data
historical_data, meta_data = ts.get_daily_adjusted(symbol='AAPL')

"""