import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

bechdel_df = pd.read_csv('my_data/updated_bechdel_4.csv')
# year_counts = bechdel_df.groupby(['year']).size()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    html.Div(children='Bechdel Test Data', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    
    html.Div(
        style={
            # would like font for radio button options to be white in this situation, but can't figure out
            # how to do that yet
            'fontColor': 'white'
        },
        children=dcc.RadioItems(
            id='radio-button-choice',
            options=[
                {'label': 'Bechdel Test passing vs. non-passing', 'value': 'Test Data'},
                {'label': 'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            # labelStyle={'fontColor': 'white'},
            # that doesn't work either
            # this is a NICE-TO-HAVE
            value='MTL'
        )      
    ),
    
    dcc.Graph(
        id='output-plot',
        figure={
            'data': [
                go.Bar(
                    x=["passing", "non-passing"],
                    y=[bechdel_df.passing.value_counts()[1], bechdel_df.passing.value_counts()[0]]),
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
])

@app.callback(
    Output(component_id='output-plot'),
    [Input(component_id='radio-button-choice')]
)
def update_plot(chosen_plot):
    

if __name__ == '__main__':
    app.run_server(debug=True)