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
    'background': '#FFFFFF',
    'text': '#000000'
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
        children=dcc.RadioItems(
            id='radio-button-choice',
            options=[
                {'label': 'Passing vs. Non-Passing Movies', 'value': 'passing'},
                {'label': 'Movies by Year', 'value': 'yearly'},
                {'label': 'Crew Gender', 'value': 'crew'}
            ]
        )      
    ),
    
    dcc.Graph(
        id='output-plot'
    ),
])

@app.callback(
    Output('output-plot', 'figure'),
    [Input('radio-button-choice', 'value')]
)
def update_plot(radio_button_choice):
    
    year_counts = bechdel_df.groupby(['year']).size()
    gender_columns = bechdel_df.columns[5:10]
    
    if radio_button_choice == 'passing':
        
        return {
            'data': [
                go.Bar(
                    x=["passing", "non-passing"],
                    y=[bechdel_df.passing.value_counts()[1], bechdel_df.passing.value_counts()[0]]
                )
            ],
            'layout': go.Layout(
                        title='Passing vs. Non-Passing Movies in Dataset',
                        yaxis={
                            'title': 'Number of Movies'
                        }
            )
        }
    
    elif radio_button_choice == 'yearly':
        
        return {
            'data': [
                go.Bar(
                    x=[year for year in year_counts.index],
                    y=[count for count in year_counts.values]
                )
            ],
            'layout': go.Layout(
                        title='Total Movies in Dataset by Year',
                        xaxis={
                            'title': 'Year'
                        },
                        yaxis={
                            'title': 'Number of Movies'
                        }
            )
        }
    
    else:
        
        return {
            'data': [
                {
                    'x': [col for col in gender_columns],
                    'y': [val for val in bechdel_df.groupby('passing')[gender_columns].sum().values[0]],
                    'name': 'Non-passing Movies',
                    'type': 'bar'
                },
                {
                    'x': [col for col in gender_columns],
                    'y': [val for val in bechdel_df.groupby('passing')[gender_columns].sum().values[1]],
                    'name': 'Passing Movies',
                    'type': 'bar'
                }
            ],
            'layout': go.Layout(
                        title='Crew Members of Underrepresented Genders in Passing vs. Non-Passing Movies',
                        xaxis={
                            'title': 'Crew Role'
                        },
                        yaxis={
                            'title': 'Gender Count'
                        }
            )
        }
    

if __name__ == '__main__':
    app.run_server(debug=True)