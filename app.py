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
                {"label": "Oscars 2019", "value": "oscars"}
            ]
        )      
    ),
    
    html.Div(
        children=[
            # html.H6("Enter movie title(s)"),
            html.P("Separate multiple movies with commas"),
            dcc.Input(
                id="text-input",
                value="Enter movie title(s)",
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
    
    elif radio_button_choice == "oscars":
        
        categories = ["All Categories", "Best Picture", "Director", "Cinematography", "Editing",
                     "Original Screenplay", "Adapted Screenplay", "Documentary - Feature", "Documentary - Short", "Production Design",
                     "Costume Design", "Makeup & Hair", "Original Score", "Original Song", "Soung Mixing", "Sound Editing",
                     "Visual Effects", "Animated Feature", "Live Action Short", "Animated Short"]

        y_male = [75,80,100,100,100,87.5,92,47,78,50,0,37.5,100,69,88,70,100,94,50,44]
        y_female = [25,20,0,0,0,12.5,8,53,22,50,100,62.5,0,31,12,30,0,6,50,56]
        
        trace1 = go.Bar(x=categories, y=y_male, name="Male")
        trace2 = go.Bar(x=categories, y=y_female, name="Female")
        
        trace3 = go.Scatter(x=categories, 
                    y=[50], 
                    name="50% Mark",
                    line=dict(
                    color="rgb(0,0,0)")
                    )
        
        return {
            
            "data": [
                trace1, trace2, trace3
            ],
            
            "layout": go.Layout(
                title="91st Academy Award Nominations for Non-Acting Categories, by Gender",
                barmode="stack",
                shapes=[
                    {
                        "type": "line",
                        "y0":50,
                        "x0":"All Categories",
                        "y1":50,
                        "x1":"Animated Short",
                        "line": {
                            "dash":"dot",
                            "color":"black"
                        }
                    }
                ],
            )
        }
    
def build_custom_df(movie_titles):
    
    # clear any pre-existing lists or dataframes
    split_movie_list = []
    stripped_movie_list = []
    row_list = []
    final_df = pd.DataFrame()
    
    if ',' not in movie_titles:
        stripped_movie = movie_titles.strip().lower()
        final_df = df[df.title == stripped_movie]
    
    else:
        split_movie_list = movie_titles.split(',')
        stripped_movie_list = [m.strip().lower() for m in split_movie_list]
        final_df = df[df.title.isin(stripped_movie_list)]
        
    return final_df
    
@app.callback(
    Output('output-table', 'data'),
    [Input('text-input', 'value')]
)
def update_table(text_input):
    
    selected_df = build_custom_df(text_input)
    
    return selected_df.to_dict("rows")
    

if __name__ == '__main__':
    app.run_server(debug=True)