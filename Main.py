#Importing alpha vantage into program after having installed it in the terminal using python -m pip install alpha_vantage
from alpha_vantage.timeseries import TimeSeries

#Creating a timeseries object, api key loaded in below
ts = TimeSeries(key='N151MRIZDCYHBXWQ', output_format='json')

#  historical_price = historical price data, ts.get_daily returns a tuple with the first element being the data and the second being metadata
# meta_data = metadata about the data, such as the last refreshed date and the interval of the data
historicalce, meta_data = ts.get_daily(symbol='AAPL')