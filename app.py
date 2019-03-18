import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd 
from dash.dependencies import Input, Output

df = pd.read_csv("my_data/updated_bechdel_4.csv")

# app = dash.Dash(__name__)

# app.layout = dash_table.DataTable(
    
#     # handle overflow data on smaller screens with multiple lines
#     style_data={"whiteSpace": "normal"},
#     css=[{
#         "selector": ".dash-cell div.dash-cell-value",
#         "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;"
#     }],

#     id="datatable-interactivity",
#     # user can remove columns
#     columns=[{"name": i, "id": i, "deletable": True} for i in df.columns],
#     data=df.to_dict("rows"),
#         editable=True,
#         filtering=True,
#         sorting=True,
#         sorting_type="multi",
#         row_selectable="multi",
#         row_deletable=True,
    #     selected_rows=[],
    # ),
    # html.Div(id='datatable-interactivity-container')
    # the following line allows for fixed headers as you scroll, but it messes a lot of other 
    # stuff up like dynamic column sizing
    # n_fixed_rows=1,
    # style_cell={'width': '150px'}
# )
    
# if __name__ == "__main__":
#     app.run_server(debug=True)

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True} for i in df.columns
        ],
        data=df.to_dict("rows"),
        editable=True,
        filtering=True,
        sorting=True,
        sorting_type="multi",
        row_selectable="multi",
        row_deletable=True,
        selected_rows=[],
        pagination_mode="fe",
            pagination_settings={
                "displayed_pages": 1,
                "current_page": 0,
                "page_size": 35,
            },
            navigation="page",
    ),
    html.Div(id='datatable-interactivity-container')
])

@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_graph(rows, derived_virtual_selected_rows):

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    if rows is None:
        dff = df
    else:
        dff = pd.DataFrame(rows)

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
                            # check if column exists - user may have deleted it
                            # If `column.deletable=False`, then you don't
                            # need to do this check.
                            "y": dff[column] if column in dff else [],
                            "type": "bar",
                            "marker": {"color": colors},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 250,
                        "margin": {"t": 10, "l": 10, "r": 10},
                    },
                },
            )
            for column in [
                "imdb_id", "passing", "score", "year", "director_gender",
                "exec_gender", "producer_gender", "writer_gender", "overall_gender",
                "budget", "revenue"
            ]
        ]
    )



if __name__ == '__main__':
    app.run_server(debug=True)