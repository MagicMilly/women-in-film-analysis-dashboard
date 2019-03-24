import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

bechdel_df = pd.read_csv('my_data/lowercase_bechdel_7.csv')

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
                {'label': 'Crew Gender', 'value': 'crew'},
            ]
        )      
    ),
    
    html.Div(
        children=[
            dcc.Input(
                id="text-input",
                value="Enter movie title",
                type="text"
            )
        ]
    ),
    
    html.Div(
        children=[
            dcc.Graph(
                id="output-plot"
            )
        ]
    ),
    
    html.Div(
        children=[
            dash_table.DataTable(
                id="output-table",
                columns=[{"name": i, "id": i} for i in bechdel_df.columns]
            )
        ]
    )
])

@app.callback(
    Output('output-plot', 'figure'),
    [Input('radio-button-choice', 'value')]
)
def update_plot(radio_button_choice):
    
    year_counts = bechdel_df.groupby(['year']).size()
    # would be more scalable to have gender columns be any column with 'gender' in name
    gender_columns = bechdel_df.columns[5:9]
    
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
    
    elif radio_button_choice == "crew":
        
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
                        title='Crew Members of Underrepresented Genders in Passing vs. Non-Passing Movies - Yes this plot is confusing',
                        xaxis={
                            'title': 'Crew Role'
                        },
                        yaxis={
                            'title': 'Gender Count'
                        }
            )
        }
    
@app.callback(
    Output('output-table', 'data'),
    [Input('text-input', 'value')]
)
def update_table(text_input):
    
    title = str(text_input).lower()
    selected_df = bechdel_df[bechdel_df.title == title]
    
    return selected_df.to_dict("rows")
    

if __name__ == '__main__':
    app.run_server(debug=True)