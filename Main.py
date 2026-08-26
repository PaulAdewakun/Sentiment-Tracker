#Importing alpha vantage into program after having installed it in the terminal using python -m pip install alpha_vantage
from alpha_vantage.timeseries import TimeSeries
import time
import os

API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")  # Load your API key from an environment variable for security

#Creating a timeseries object, api key loaded in below
ts = TimeSeries(key=API_KEY, output_format='json')





# historical_data = historical price data, ts.get_daily_adjusted returns a tuple with the first element being the data and the second being metadata
# meta_data = metadata about the data, such as the last refreshed date and the interval of the data
historical_data, meta_data = ts.get_daily_adjusted(symbol='AAPL')