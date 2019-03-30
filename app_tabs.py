import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import plotly.graph_objs as go

from dash.dependencies import Input, Output, State

# for use with html.Table - Tab 2
condensed_bechdel = pd.read_csv('my_data/condensed_bechdel_7.csv')
# for use in interactive DataTable - Tab 3
bechdel_df = pd.read_csv('my_data/bechdel_8_for_datatable.csv')


oscar_categories = ["All Categories", "Best Picture", "Director", "Cinematography", "Editing",
              "Original Screenplay", "Adapted Screenplay", "Documentary - Feature", "Documentary - Short", "Production Design",
              "Costume Design", "Makeup & Hair", "Original Score", "Original Song", "Sound Mixing", "Sound Editing", 
              "Visual Effects", "Animated Feature", "Live Action Short", "Animated Short"]

# Percentages of nominees by gender
y_male = [75,80,100,100,100,87.5,92,47,78,50,0,37.5,100,69,88,70,100,94,50,44]
y_female = [25,20,0,0,0,12.5,8,53,22,50,100,62.5,0,31,12,30,0,6,50,56]

colors = {
    'background': '#FFFFFF',
    'text': '#000000',
    'passing': '#90EE90',
    'failing': '#E78383'
}

PAGE_SIZE = 10

# Style passing movies with green color and non-passing movies with red for easy identification (for use with html.Table)
def cell_style(value):
    style = {}
    if value > 0:
        style = {
            'backgroundColor': colors['passing']
        }
    else:
        style = {
            'backgroundColor': colors['failing']
        }   
    return style

# Use cell color styling for non-interactive html.Table of Tab Two (Choose Your Movie) 
def generate_table(dataframe, max_rows=20):
    rows = []
    for i in range(min(len(dataframe), max_rows)):
        row = []
        for col in dataframe.columns:
            if col == 'passing':
                value = dataframe.iloc[i][col]
                style = cell_style(value)
                row.append(html.Td(value, style=style))
            elif col == 'director':
                value = dataframe.iloc[i][col]
                style = cell_style(value)
                row.append(html.Td(value, style=style))
            elif col == 'writer':
                value = dataframe.iloc[i][col]
                style = cell_style(value)
                row.append(html.Td(value, style=style))
            elif col == 'producer':
                value = dataframe.iloc[i][col]
                style = cell_style(value)
                row.append(html.Td(value, style=style))
            elif col == 'overall':
                value = dataframe.iloc[i][col]
                style = cell_style(value)
                row.append(html.Td(value, style=style))
            else:
                value = dataframe.iloc[i][col]
                row.append(html.Td(value))
        rows.append(html.Tr(row))
    return html.Table([html.Tr([html.Th(col) for col in dataframe.columns])] + rows)

app = dash.Dash()

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


app.layout = html.Div([
    html.H1('Women in Film & The Bechdel Test', style={
            'textAlign': 'center', 'margin': '48px 0', 'fontFamily': 'system-ui'}),
    
    dcc.Tabs(id="tabs", children=[
        
        dcc.Tab(label='Academy Awards', children=[
            html.Div([
                dcc.Graph(
                    id='oscars-2019',
                    figure={
                        'data': [
                            go.Bar(x=oscar_categories, y=y_male, name="Male"),
                            go.Bar(x=oscar_categories, y=y_female, name="Female"),
                        ],
                        'layout': 
                            go.Layout(
                                title="Gender Percentages for 2019 Academy Award Nominees in Non-Acting Categories",
                                barmode="stack",
                                margin={'l': 100, 'b': 100, 't': 100, 'r': 100}
                            )
                    }
                )
            ])
        ]),
        
        dcc.Tab(label='Choose Your Own Movie', children=[
            html.Div([
                html.H3("Movies in the Bechdel Test Dataset"),
                html.P("""
                    Enter a movie tittle or use the dropdown menu to select one or more movies to see if they passed the Bechdel Test. A
                    green box in the passing column indicates that a movie passed the test. For the director, writer, and producer
                    column, a green box indicates that there was at least one crew member in that role of an underrepresented gender. The
                    overall column represents the sum of the crew columns. If a movie had at least one director, writer, and producer
                    of an underrepresented gender, that movie would have the maximum overall value of 3.
                    """),
                dcc.Dropdown(
                    id='dropdown',
                    options=[
                        {'label': i, 'value': i} for i in condensed_bechdel.title.unique()
                    ], 
                    multi=True, 
                    placeholder='Filter by movie...'),
                html.Div(id='table-container')
            ])
        ]),
        
        dcc.Tab(label='Interactive DataTable - Explore Test Scores & Crew Gender', children=[
            html.Div([
                html.H3("Bechdel Test points explained"),
                html.P("""
                    The score column represents how many points a movie scored on the Bechdel Test. A 3-point score is considered
                    passing. Points are awarded as follows:
                    """),
                html.P("1 point for two named female characters"),
                html.P("2 points for two named female characters who talk to each other"),
                html.P("3 points for two named female characters who talk to each other about something other than a man"),
                html.P("""In the director, writer, and producer columns, a 1 signifies that there was at least one crew member 
                    in that role of an underrepresented gender. The overall column is the sum of those points. A movie that had at
                    least one director, writer, and producer of an underrepresented gender would have a value of 3 in the overall
                    column. Note that the Bechdel Test is only concerned with the movie's content. The crew member, budget, and revenue
                    columns were added to the data that was scraped from the Bechdel Test website.
                    """),
                dash_table.DataTable(
                    id='datatable-interactivity',
                    columns=[
                        {"name": i, "id": i, "deletable": False} for i in bechdel_df.columns
                    ],
                    data=bechdel_df.to_dict("rows"),
                    editable=True,
                    filtering=True,
                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['year', 'title']
                    ] + [
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ],
                    sorting=True,
                    sorting_type="multi",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_rows=[],
                    pagination_mode="fe",
                    pagination_settings={
                        "displayed_pages": 1,
                        "current_page": 0,
                        "page_size": 20,
                    },
                    navigation="page",
                ),
        html.Div(id='datatable-interactivity-container')
            ]
        )        
    ]),
    ],
        style={
        'fontFamily': 'system-ui'
    },
        content_style={
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'borderBottom': '1px solid #d6d6d6',
        'padding': '44px'
    },
        parent_style={
        'maxWidth': '1000px',
        'margin': '0 auto'
    }
    )
]) 

# Callback for Tab Two - Choose Your Movie
@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table(dropdown_value):
    if dropdown_value is None:
        return generate_table(condensed_bechdel)
    dff = condensed_bechdel[condensed_bechdel.title.str.contains('|'.join(dropdown_value))]
    return generate_table(dff)

# Callback for Tab Three - Graph Output from DataTable
@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_viewport_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_graph(derived_viewport_data, derived_virtual_selected_rows):

    # Output graph will only contain rows from the current page.
    # If rows are deleted, new movies will populate the table to keep the page at preset size and appear in graph.
    dff = pd.DataFrame(derived_viewport_data)
        
    # Rows/movies selected by user will change color in graph
    colors = []
    for i in range(len(dff)):
        if i in derived_virtual_selected_rows:
            colors.append("#7FDBFF")
        else:
            colors.append("#0074D9")
    
    return html.Div(
        [
            dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": dff["title"],
                            # If column.deletable=True,
                            # check if column exists - user may have deleted it
                            # "y": dff[column] if column in dff else [],
                            "y": dff[column],
                            "type": "bar",
                            "marker": {"color": colors},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 300,
                        "margin": {"t": 75, "l": 10, "r": 10, "b":100},
                        "title": column
                    },
                },
            )
            for column in ["score", "passing", "director", "writer", "producer", "overall"]
        ]
    )
    


if __name__ == '__main__':
    app.run_server(debug=True)