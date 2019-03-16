import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import plotly.graph_objs as go

app = dash.Dash()

# df = pd.read_csv('my_data/practice_data/bechdel_no_zeros.csv')

# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }

app.layout = html.Div('Dash tutorial with sentdex')

if __name__ == '__main__':
    app.run_server(debug=True)