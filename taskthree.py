import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("tasktwo_output.csv")

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# -----------------------------
# Create line chart
# -----------------------------
fig = px.line(
    df,
    x="Date",
    y="Sales",
    labels={
        "Date": "Date",
        "Sales": "Total Sales"
    },
    title="Pink Morsel Sales Over Time"
)

# -----------------------------
# Price increase marker (SAFE WAY)
# -----------------------------
price_increase_date = pd.to_datetime("2021-01-15")

# Vertical line ONLY (no annotation here)
fig.add_shape(
    type="line",
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(color="red", width=2, dash="dash")
)

# Manual annotation (THIS avoids the bug)
fig.add_annotation(
    x=price_increase_date,
    y=1,
    xref="x",
    yref="paper",
    text="Price Increase<br>15 Jan 2021",
    showarrow=False,
    yanchor="bottom",
    font=dict(color="red")
)

# -----------------------------
# Dash app
# -----------------------------
app = Dash(__name__)

app.layout = html.Div(
    style={"padding": "40px"},
    children=[
        html.H1(
            "Soul Foods – Pink Morsel Sales Visualiser",
            style={"textAlign": "center"}
        ),
        html.P(
            "The red dashed line marks the Pink Morsel price increase on 15 January 2021.",
            style={"textAlign": "center"}
        ),
        dcc.Graph(figure=fig)
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
