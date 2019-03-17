import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas as pd 
import pandas_datareader.data as web
# import plotly.graph_objs as go

from dash.dependencies import Input, Output

app = dash.Dash()

# df.reset_index(inplace=True)
# df.set_index("Date", inplace=True)
# df = df.drop("Symbol", axis=1)

app.layout = html.Div(children=[
    
    html.Div(children='''
        symbol to graph:
    '''),

    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph')
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
    )

def update_graph(input_data):
    
    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(input_data, 'iex', start, end)

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df.close, 'type': 'line', 'name': 'stock'},
            ],
            'layout': {
                'title': 'stock'
            }
        }
    )
    

if __name__ == '__main__':
    app.run_server(debug=True)