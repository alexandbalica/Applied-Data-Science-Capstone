import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
)

spacex_df = pd.read_csv(DATA_URL)

# Make outcome meaning explicit
spacex_df["Landing Outcome"] = spacex_df["class"].map(
    {1: "Success", 0: "Failed"}
)

min_payload = spacex_df["Payload Mass (kg)"].min()
max_payload = spacex_df["Payload Mass (kg)"].max()


# ---------------------------------------------------------
# Dash application
# ---------------------------------------------------------

app = dash.Dash(__name__)

dropdown_options = [
    {"label": "All Sites", "value": "ALL"},
    {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
    {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
    {"label": "KSC LC-39A", "value": "KSC LC-39A"},
    {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
]


# ---------------------------------------------------------
# Layout
# ---------------------------------------------------------

app.layout = html.Div(
    style={
        "maxWidth": "1600px",
        "margin": "0 auto",
        "padding": "20px 30px",
        "fontFamily": "Arial, sans-serif",
    },
    children=[

        html.H1(
            "SpaceX First-Stage Landing Dashboard",
            style={
                "textAlign": "center",
                "marginBottom": "25px",
            },
        ),

        # Controls
        html.Div(
            style={
                "display": "flex",
                "gap": "30px",
                "alignItems": "end",
                "marginBottom": "20px",
            },
            children=[

                html.Div(
                    style={"flex": "1"},
                    children=[
                        html.Label(
                            "Launch Site",
                            style={"fontWeight": "bold"},
                        ),

                        dcc.Dropdown(
                            id="site-dropdown",
                            options=dropdown_options,
                            value="ALL",
                            clearable=False,
                        ),
                    ],
                ),

                html.Div(
                    style={"flex": "2"},
                    children=[
                        html.Label(
                            "Payload Mass Range (kg)",
                            style={"fontWeight": "bold"},
                        ),

                        dcc.RangeSlider(
                            id="payload-slider",
                            min=0,
                            max=max_payload,
                            step=500,
                            marks={
                                0: "0",
                                2500: "2,500",
                                5000: "5,000",
                                7500: "7,500",
                                10000: "10,000",
                            },
                            value=[min_payload, max_payload],
                            tooltip={
                                "placement": "bottom",
                                "always_visible": False,
                            },
                        ),
                    ],
                ),
            ],
        ),

        # Main analysis area
        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "alignItems": "stretch",
            },
            children=[

                # Pie chart
                html.Div(
                    style={
                        "width": "34%",
                        "border": "1px solid #ddd",
                        "borderRadius": "8px",
                        "padding": "5px",
                    },
                    children=[
                        dcc.Graph(
                            id="success-pie-chart",
                            config={
                                "displaylogo": False,
                                "toImageButtonOptions": {
                                    "format": "png",
                                    "filename": "landing_outcomes",
                                    "height": 900,
                                    "width": 1200,
                                    "scale": 2,
                                },
                            },
                        )
                    ],
                ),

                # Scatter chart
                html.Div(
                    style={
                        "width": "66%",
                        "border": "1px solid #ddd",
                        "borderRadius": "8px",
                        "padding": "5px",
                    },
                    children=[
                        dcc.Graph(
                            id="success-payload-scatter-chart",
                            config={
                                "displaylogo": False,
                                "toImageButtonOptions": {
                                    "format": "png",
                                    "filename": "payload_vs_landing_outcome",
                                    "height": 900,
                                    "width": 1600,
                                    "scale": 2,
                                },
                            },
                        )
                    ],
                ),
            ],
        ),
    ],
)


# ---------------------------------------------------------
# Pie chart callback
# ---------------------------------------------------------

@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value"),
)
def get_pie_chart(selected_site):

    if selected_site == "ALL":
        df = spacex_df
        title = "First-Stage Landing Outcomes — All Sites"
    else:
        df = spacex_df[
            spacex_df["Launch Site"] == selected_site
        ]
        title = f"First-Stage Landing Outcomes — {selected_site}"

    counts = (
        df["Landing Outcome"]
        .value_counts()
        .rename_axis("Outcome")
        .reset_index(name="Count")
    )

    fig = px.pie(
        counts,
        names="Outcome",
        values="Count",
        hole=0.35,
        title=title,
        color="Outcome",
        color_discrete_map={
            "Success": "#2ca02c",
            "Failed": "#d62728",
        },
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=70, b=20),
        legend_title_text="Landing Outcome",
    )

    return fig


# ---------------------------------------------------------
# Scatter chart callback
# ---------------------------------------------------------

@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [
        Input("site-dropdown", "value"),
        Input("payload-slider", "value"),
    ],
)
def update_scatter(selected_site, payload_range):

    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= low)
        & (spacex_df["Payload Mass (kg)"] <= high)
    ].copy()

    if selected_site != "ALL":
        filtered_df = filtered_df[
            filtered_df["Launch Site"] == selected_site
        ]

    site_label = (
        "All Sites"
        if selected_site == "ALL"
        else selected_site
    )

    fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        title=f"Payload Mass vs. First-Stage Landing Outcome — {site_label}",
        labels={
            "Payload Mass (kg)": "Payload Mass (kg)",
            "class": "Landing Outcome",
            "Booster Version Category": "Booster Version",
        },
        hover_data=[
            "Launch Site",
            "Landing Outcome",
        ],
    )

    # Replace 0 / 1 with meaningful labels
    fig.update_yaxes(
        tickmode="array",
        tickvals=[0, 1],
        ticktext=["Failed", "Success"],
        range=[-0.15, 1.15],
    )

    fig.update_traces(
        marker=dict(size=10, opacity=0.8)
    )

    fig.update_layout(
        height=500,
        margin=dict(l=50, r=20, t=70, b=50),
        legend_title_text="Booster Version",
    )

    return fig


# ---------------------------------------------------------
# Run application
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)