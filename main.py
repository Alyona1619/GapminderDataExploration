from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_draggable


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# external CSS stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)


# style_dashboard = {
#     "height": '100%',
#     "width": '100%',
#     "display": "flex",
#     "flex-direction": "column",
#     "flex-grow": "0"
# }

full_names = {
    'pop': 'Population',
    'lifeExp': 'Life Expectancy',
    'gdpPercap': 'GDP per Capita'
}


@app.callback(
    Output('graph-content', 'figure'),
    Output('bar-chart', 'figure'),
    Output('bubble-chart', 'figure'),
    Output('top-pop-chart', 'figure'),
    Output('continent-pop-chart', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('y-axis-selection', 'value'),
    Input('x-axis-selection', 'value'),
    Input('bubble-size-selection', 'value'),
    Input('y-axis-bubble-selection', 'value'),  # bubble chart y-axis
    Input('year-slider', 'value')
)
def update_graph(selected_countries, y_axis, x_axis, bubble_size, bubble_y_axis, selected_year):
    dff = df[df['country'].isin(selected_countries)]
    fig_line = px.line(dff, x='year', y=y_axis, color='country', title=f"Trend of {full_names.get(y_axis, y_axis)} over years")
    fig_bar = px.bar(dff[dff['year'] == selected_year], x='country', y=y_axis, title=f"{full_names.get(y_axis,y_axis)} in {selected_year} for selected countries")

    fig_bubble = px.scatter(dff[dff['year'] == selected_year], x=x_axis, y=bubble_y_axis, size=bubble_size,
                            color='country',
                            title=f"{full_names.get(bubble_y_axis, bubble_y_axis)} vs {full_names.get(x_axis, x_axis)} with bubble size of {full_names.get(bubble_size, bubble_size)}")

    top_countries_pop = df[df['year'] == selected_year].groupby('country')['pop'].max().sort_values(
        ascending=False).head(15)
    top_countries_pop = top_countries_pop.reset_index()
    fig_top_pop = px.bar(top_countries_pop, x='country', y='pop',
                         title=f"Top-15 Countries by Population in {selected_year}")

    fig_continent_pop = px.pie(df[df['year'] == selected_year], values='pop', names='continent',
                               title=f'Population by Continent in {selected_year}')

    return fig_line, fig_bar, fig_bubble, fig_top_pop, fig_continent_pop


app.layout = html.Div([
    html.H1(children='Gapminder Data Exploration', style={'textAlign': 'center'}),
    dash_draggable.ResponsiveGridLayout(
        id='draggable',
        children=[
            html.Div(children=[
                dcc.Dropdown(options=[{'label': country, 'value': country} for country in df.country.unique()],
                             multi=True,
                             value=['Canada', 'United States', 'China', 'Japan', 'Albania', 'Zimbabwe'], id='dropdown-selection',
                             style={"width": '80%'}),
                dcc.Dropdown(
                    options=[{'label': col, 'value': col} for col in df.select_dtypes(include='number').columns if col!='year'],
                    value='lifeExp', id='y-axis-selection', style={"width": '50%', "margin-top": '4px'}),
                html.Div(children=[
                    dcc.Graph(id='graph-content'),
                    dcc.Graph(id='bar-chart'),
                ], style={
                    "height": '100%',
                    "width": '100%',
                    "display": "flex",
                    "flex-direction": "row",
                    "flex-grow": "1"
                }),
            ], style={  # первые две
                "height": '100%',
                "width": '100%',
                "display": "flex",
                "flex-direction": "column",
                "flex-grow": "1",
                "overflow": "auto"
            }),
#
            html.Div(children=[
                html.Div(children=[
                    dcc.Slider(
                        id='year-slider',
                        min=df['year'].min(),
                        max=df['year'].max(),
                        value=df['year'].max(),
                        marks={str(year): str(year) for year in df['year'].unique() if year % 5 == 0 or year==1950 or year==2007},
                        step=None
                    )
                ], style={  }# слайдер по годам
                ),
                html.Div(children=[
                    html.Div(children=[
                        dcc.Dropdown(
                            options=[{'label': col, 'value': col} for col in
                                     df.select_dtypes(include='number').columns if col != 'year'],
                            value='pop', id='x-axis-selection', style={"width": '100%', "margin-top": '60px'}),
                        dcc.Dropdown(
                            options=[{'label': col, 'value': col} for col in
                                     df.select_dtypes(include='number').columns if col != 'year'],
                            value='lifeExp', id='bubble-size-selection', style={"width": '100%', "margin-top": '4px'}),
                        dcc.Dropdown(
                            options=[{'label': col, 'value': col} for col in
                                     df.select_dtypes(include='number').columns],
                            value='gdpPercap', id='y-axis-bubble-selection', style={"width": '100%', "margin-top": '4px'}),

                    ], style={"height": '100%',
                              "width": '20%',
                              "display": "flex",
                              "flex-direction": "column",
                              "flex-grow": "1",
                              "float": "right"}),

                    html.Div(children=[dcc.Graph(id='bubble-chart', style={"width": '100%'})], style={"width": '80%'}),
                ], style={  # пузырек
                    "width": '100%',
                    "display": "flex",
                    "flex-direction": "row",
                    "flex-grow": "0"
                }),
                html.Div(children=[
                    dcc.Graph(id='top-pop-chart'),
                    dcc.Graph(id='continent-pop-chart'),
                ], style={  # круговая и топ 15
                    "width": '100%',
                    "display": "flex",
                    "flex-direction": "row",
                    "flex-grow": "1"}
                )],
                style={
                    "width": '100%',
                    "display": "flex",
                    "flex-direction": "column",
                    "flex-grow": "0",
                    "overflow": "auto"
                })

        ], style={
            "height": '100%',
            "width": '100%',
            "display": "flex",
            "flex-direction": "column",
            "flex-grow": "0"
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
