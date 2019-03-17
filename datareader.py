import datetime
import pandas as pd 
import pandas_datareader.data as web

start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2017, 2, 8)

f = web.DataReader('F', 'iex', start, end)

print(f.head())