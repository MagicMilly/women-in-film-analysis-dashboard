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
bechdel_df = pd.read_csv('my_data/lowercase_bechdel_7.csv')


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
    html.H1('The Bechdel Test & Women in the Film Industry', style={
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
        
        dcc.Tab(label='Choose Your Movie', children=[
            html.Div([
                html.H3("Movies in the Bechdel Test Dataset"),
                html.P("""
                    Enter a movie tittle or use the dropdown menu to select one or more movies to see if they passed the Bechdel Test. A
                    green box in the "passing" column indicates that a movie passed the test. For the "director", "writer", and "producer"
                    column, a green box indicates that there was at least one crew member in that role of an underrepresented gender. The
                    "overall" column represents the sum of the crew columns. If a movie had at least one director, writer, and producer
                    of an underrepresented gender, that movie would have the maximum "overall" value of 3.
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
        
        dcc.Tab(label='Interactive DataTable', children=[
            html.Div([
                html.H1("This is the content in tab 3"),
                dash_table.DataTable(
                    id='table-paging-and-sorting',
                    columns=[
                        {'name': i, 'id': i, 'deletable': True} for i in bechdel_df.columns
                    ],
                    style_cell_conditional=
                    [
                    {
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['year', 'title']
                    ],
                    style_as_list_view=True,
                    pagination_settings={
                        'current_page': 0,
                        'page_size': PAGE_SIZE
                    },
                    pagination_mode='be',
                    sorting='be',
                    sorting_type='single',
                    sorting_settings=[],
                    editable=True
                )]
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

# Table for Tab Two - Choose Your Movie
@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table(dropdown_value):
    if dropdown_value is None:
        return generate_table(condensed_bechdel)
    dff = condensed_bechdel[condensed_bechdel.title.str.contains('|'.join(dropdown_value))]
    return generate_table(dff)

# Tab Three - Interactive DataTable
@app.callback(
    Output('table-paging-and-sorting', 'data'),
    [Input('table-paging-and-sorting', 'pagination_settings'),
    Input('table-paging-and-sorting', 'sorting_settings')])
def update_graph(pagination_settings, sorting_settings):
    if len(sorting_settings):
        dff = bechdel_df.sort_values(
        sorting_settings[0]['column_id'],
        ascending=sorting_settings[0]['direction'] == 'asc',
        inplace=False)
    else:
        # No sort is applied
        dff = bechdel_df
    return dff.iloc[
        pagination_settings['current_page'] * pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1) * pagination_settings['page_size']
    ].to_dict('rows')


if __name__ == '__main__':
    app.run_server(debug=True)

