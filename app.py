import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from engine import export_dataframe

dfi = export_dataframe()

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Reality-Rewired Dashboard"

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Reality-Rewired Dashboard", className="app__header__title"),
                    ],
                    className="app__header__desc",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("About", className="link-button"),
                            href="https://plotly.com/get-demo/",
                        ),
                        html.A(
                            html.Img(
                                src=app.get_asset_url("dash-new-logo.png"),
                                className="app__menu__img",
                            ),
                            href="https://plotly.com/dash/",
                        ),
                    ],
                    className="app__header__logo",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [html.H6("Heart Rate Sensor Readings", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="heart-rate",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                        dcc.Interval(
                            id="heart-rate-update",
                            interval=1000,
                            n_intervals=0,
                        ),
                    ],
                    className="two-thirds column wind__speed__container",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "GSR Sensor Readings",
                                            className="graph__title",
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="gsr-reading-graph",
                                    figure=dict(
                                        layout=dict(
                                            plot_bgcolor=app_color["graph_bg"],
                                            paper_bgcolor=app_color["graph_bg"],
                                        )
                                    ),
                                ),
                            ],
                            className="graph__container first",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container",
)



@app.callback(
    Output("heart-rate", "figure"), [Input("heart-rate-update", "n_intervals")]
)
def gen_heart_rate(interval):
    """
    Generate the wind speed graph.

    :params interval: update the graph based on an interval
    """

    trace = dict(
        type="scatter",
        y=dfi["pulsedetect"],
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        height=700,
        xaxis={
            "range": [175,0],
            "showline": True,
            "zeroline": False,
            "fixedrange": False,
            "tickvals": [0, 50, 100, 150, 200],
            "ticktext": ["200", "150", "100", "50", "0"],
            "title": "Time Elapsed (sec)",
        },
    )

    return dict(data=[trace], layout=layout)

@app.callback(
    Output("gsr-reading-graph", "figure"),
    [Input("heart-rate-update", "n_intervals")],
    [
        State("heart-rate", "figure"),
    ],
)
def gen_wind_histogram(a,b):
    trace = dict(
        type="scatter",
        y=dfi["gsrdetect"],
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        height=700,
        xaxis={
            "range": [100,0],
            "showline": True,
            "zeroline": False,
            "fixedrange": False,
            "tickvals": [0, 50, 100, 150, 200],
            "ticktext": ["200", "150", "100", "50", "0"],
            "title": "Time Elapsed (sec)",
        },
    )

    return dict(data=[trace], layout=layout)

if __name__ == "__main__":
    app.run_server(debug=True)
