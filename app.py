from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from engine import export_heartrate

app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Reality-Rewired Dashboard"
server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H1("Reality-Rewired Dashboard", className="font-bold text-2xl"),
                    ],
                    className="",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("About", className=""),
                            href="https://plotly.com/get-demo/",
                        ),
                        html.A(
                            html.Img(
                                src=app.get_asset_url(""),
                                className="",
                            ),
                            href="https://plotly.com/dash/",
                        ),
                    ],
                    className="",
                ),
            ],
            className="",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [html.H6("Heart Rate Sensor Readings", className="")]
                        ),
                        dcc.Graph(
                            id="heart-rate",
                            figure=dict(
                                # layout=dict(
                                #     plot_bgcolor=app_color[""],
                                #     paper_bgcolor=app_color[""],
                                # )
                            ),
                        ),
                        dcc.Interval(
                            id="heart-rate-update",
                            interval=4000,
                            n_intervals=1000,
                        ),
                    ],
                    className="",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "GSR Sensor Readings",
                                            className="",
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
                            className="",
                        ),
                    ],
                    className="",
                ),
            ],
            className="",
        ),
    ],
    className="container mx-auto mt-4",
)


@app.callback(
    Output("heart-rate", "figure"), [Input("heart-rate-update", "n_intervals")]
)
def gen_heart_rate(interval):
    """
    Generate the heart rate graph.

    :params interval: update the graph based on an interval
    """
    from engine import export_dataframe
    dfi = export_dataframe()
    heartrate = export_heartrate()
    print(heartrate)    

    trace = dict(
        type="scatter",
        y=dfi["PPG"],
        # y=[1,2,3,4,5],
        hoverinfo="skip",
        mode="lines",
    )

    layout = dict(
        height=700,
        xaxis={
            "showline": True,
            "zeroline": False,
            "fixedrange": False,
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
def gen_wind_histogram(a, b):
    from engine import export_dataframe
    dfi = export_dataframe()

    trace = dict(
        type="scatter",
        y=dfi["GSR"],
        mode="lines",
    )

    layout = dict(
        height=700,
        xaxis={
            "showline": True,
            "zeroline": False,
            "fixedrange": False,
            "title": "Time Elapsed (sec)",
        },
    )

    return dict(data=[trace], layout=layout)

if __name__ == "__main__":
    app.run_server(debug=True)
