import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Create the app
app = dash.Dash(__name__)

# Define the navbar layout
navbar = html.Div(
    [
        dcc.Link("Gapminder", href="/gapminder", className="nav-link"),
        dcc.Link("Iris", href="/iris", className="nav-link"),
        dcc.Link("Tips", href="/tips", className="nav-link"),
    ],
    className="navbar"
)

# Define the content layout
content = html.Div(id="page-content", className="content")

# Define the app layout
app.layout = html.Div([dcc.Location(id="url"), navbar, content])

# Load the datasets
gapminder_df = px.data.gapminder()
iris_df = px.data.iris()
tips_df = px.data.tips()

def create_section_header(title):
    return html.H2(title, className="section-header")

# Define the Gapminder page layout
gapminder_layout = html.Div(
    [
        create_section_header("Life Expectancy vs GDP per Capita"),
        dcc.Graph(figure=px.scatter(
            gapminder_df,
            x="gdpPercap",
            y="lifeExp",
            animation_frame="year",
            animation_group="country",
            size="pop",
            color="continent",
            hover_name="country",
            log_x=True, 
            size_max=55,
            range_x=[100,100000],
            range_y=[25,90])
        ),
        create_section_header("Population by Year and Continent"),
        dcc.Graph(figure=px.area(
            gapminder_df,
            x="year",
            y="pop",
            color="continent",
            line_group="country",
            hover_name="country",
            line_shape="spline",
            title="Population by Year and Continent"
        ))
    ]
)

# Define the Tips page layout
iris_layout = html.Div(
    [
        create_section_header("Sepal Length vs Sepal Width"),
        dcc.Graph(figure=px.scatter(
            iris_df,
            x="sepal_width",
            y="sepal_length",
            color="species",
            size="petal_length",
            hover_name="species",
            title="Sepal Length vs Sepal Width"
        )),
        create_section_header("Petal Length Distribution"),
        dcc.Graph(figure=px.histogram(
            iris_df,
            x="petal_length",
            color="species",
            marginal="violin",
            hover_name="species",
            title="Petal Length Distribution"
        ))
    ]
)

# Define the Tips page layout
tips_layout = html.Div(
    [
        create_section_header("Total Bill vs Tip Amount"),
        dcc.Graph(figure=px.scatter(
            tips_df,
            x="total_bill",
            y="tip",
            color="sex",
            trendline="ols",
            hover_name="sex",
            title="Total Bill vs Tip Amount"
        )),
        create_section_header("Tips by Day and Time"),
        dcc.Graph(figure=px.bar(
            tips_df,
            x="day",
            y="tip",
            color="time",
            barmode="group",
            hover_name="time",
            title="Tips by Day and Time"
        )),
        create_section_header("Heatmap"),
        dcc.Graph(figure=px.density_heatmap(
            tips_df,
            x="total_bill",
            y="tip",
            facet_row="sex",
            facet_col="smoker"
        )),
    ]
)

# Callback to render page content
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/gapminder":
        return gapminder_layout
    elif pathname == "/iris":
        return iris_layout
    elif pathname == "/tips":
        return tips_layout
    else:
        return html.H2("Page not found")


if __name__ == "__main__":
    app.run_server(debug=True)
