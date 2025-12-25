import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("formatted_output.csv")

df["Date"] = pd.to_datetime(df["Date"])
df["Region"] = df["Region"].str.lower()

# -----------------------------
# Dash app
# -----------------------------
app = Dash(__name__)

app.layout = html.Div(
    className="app-container",
    children=[
        html.H1(
            "Soul Foods – Pink Morsel Sales Visualiser",
            className="header"
        ),

        html.P(
            "Explore how Pink Morsel sales changed over time and across regions. "
            "The red dashed line marks the price increase on 15 January 2021.",
            className="subtext"
        ),

        # -----------------------------
        # Controls
        # -----------------------------
        html.Div(
            className="controls",
            children=[
                html.Label(
                    "Select Region:",
                    style={"fontWeight": "bold", "marginBottom": "10px"}
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
            ],
        ),

        # -----------------------------
        # Graph
        # -----------------------------
        html.Div(
            className="graph-card",
            children=[
                dcc.Graph(id="sales-line-chart")
            ],
        ),
    ],
)

# -----------------------------
# Callback
# -----------------------------
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["Region"] == selected_region]

    filtered_df = filtered_df.sort_values("Date")

    fig = px.line(
        filtered_df,
        x="Date",
        y="Sales",
        labels={
            "Date": "Date",
            "Sales": "Total Sales"
        },
        title="Pink Morsel Sales Over Time"
    )

    # Price increase marker (safe method)
    price_increase_date = pd.to_datetime("2021-01-15")

    fig.add_shape(
        type="line",
        x0=price_increase_date,
        x1=price_increase_date,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="red", width=2, dash="dash"),
    )

    fig.add_annotation(
        x=price_increase_date,
        y=1,
        xref="x",
        yref="paper",
        text="Price Increase<br>15 Jan 2021",
        showarrow=False,
        yanchor="bottom",
        font=dict(color="red"),
    )

    return fig

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
