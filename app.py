import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas as pd 
import pandas_datareader.data as web
import plotly.graph_objs as go

from dash.dependencies import Input, Output

start = datetime.datetime(2015,1,1)
end = datetime.datetime(2018,2,8)

df = web.DataReader('TSLA', 'google', start, end)

print(df.head())

# if __name__ == '__main__':
#     app.run_server(debug=True)