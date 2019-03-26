import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

df = pd.read_csv('my_data/lowercase_bechdel_7.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def generate_table(dataframe, max_rows=25):
    
    return html.Table(
        
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
                children=[
                    html.H4(children='Movies in Bechdel Test Dataset'),
            
                    dcc.Dropdown(
                        id='dropdown', 
                        options=[
                            {'label': i, 'value': i} for i in df.title.unique()
                        ], multi=True, placeholder='Filter by movie...'),
    
                    html.Div(id='table-container')
                ]
)

@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table(dropdown_value):
    
    if dropdown_value is None:
        
        return generate_table(df)

    dff = df[df.title.str.contains('|'.join(dropdown_value))]
    
    return generate_table(dff)

if __name__ == '__main__':
    app.run_server(debug=True)