import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("formatted_output.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Region"] = df["Region"].str.lower()

# Create Dash app
app = Dash(__name__)

app.layout = html.Div(
    className="app-container",
    children=[
        html.H1(
            "Soul Foods – Pink Morsel Sales Visualiser",
            id="app-header"
        ),

        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"},
            ],
            value="all",
            inline=True,
        ),

        dcc.Graph(id="sales-line-chart"),
    ],
)

@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(region):
    if region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["Region"] == region]

    fig = px.line(
        filtered_df.sort_values("Date"),
        x="Date",
        y="Sales",
        title="Pink Morsel Sales Over Time",
    )

    price_increase_date = pd.to_datetime("2021-01-15")

    fig.add_shape(
        type="line",
        x0=price_increase_date,
        x1=price_increase_date,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="red", dash="dash"),
    )

    return fig
