from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from engine import export_heartrate, heart_rate_update

external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}], external_scripts=external_script,
)
app.title = "Reality-Rewired Dashboard"
server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

heart_rate = 0;

app.layout = html.Div(
    [
        html.Div(
            [html.Div(
                [
                    html.Img(
                        src="https://raw.githubusercontent.com/tejabalu/OrateVR/5cd3e04c92d4be4ebb1f870b2f1f5b304cfe72c8/assets/orateVR%20logo-01-02.svg",
                        className="object-cover h-56 w-56 flex-none",
                    ),
                    html.Div(
                        [], className="grow",
                    ),
                    html.Div(
                        [
                            html.H2("OrateVR Realtime Dashboard", className="h2 block py-2 font-bold text-3xl text-gray-800"),
                            html.P("Done as part of Hardware-Software Lab...", className="text-lg text-gray-600"),
                        ],
                        className="flex-none w-1/3 text-right",
                    ),
                ],
                className="flex items-center justify-center w-full",
            ),
            ], className="flex pb-8",
        ),
        html.P("Sensor Readings from OrateVR wearable:", className="block p-4 text-3xl text-gray-600"),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [html.H6("PPG (heart rate) Sensor Readings", className="h2 py-2 text-2xl text-gray-800 pl-4")],
                        ),
                        dcc.Graph(
                            id="heart-rate-graph",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ), style={"height": "500px"},
                        ),
                        dcc.Interval(
                            id="heart-rate-update",
                            interval=4000,
                            n_intervals=1000,
                        ),
                    ],
                    className="w-1/2 h-full m-4 bg-white shadow-2xl",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("GSR Sensor Readings", className="h2 py-2 text-2xl text-gray-800 pl-4",)
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
                        ),
                    ],
                    className="w-1/2 h-full m-4 bg-white shadow-2xl",
                ),
            ],
            className="flex width-full",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [html.H6("Heart Rate", className="flex-none h2 py-2 text-2xl text-gray-800")],
                        ),
                        html.Div(
                            [
                                html.H6(heart_rate, className="grow text-[120px] font-medium text-gray-600 block  text-center"),
                                html.H6("Beats per minute", className="grow text-lg font-medium text-gray-600 block text-center"),
                            ]
                        ),
                    ],
                    className="flex flex-col w-1/4 h-full p-4 m-4 bg-white shadow-2xl",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("Stress Levels", className="h2 py-2 text-2xl text-gray-800 pt-auto",)
                                    ],
                                ),
                            ],
                        ),
                    ],
                    className="grow items-center p-4 bg-white shadow-2xl m-4",
                ),
            ],
            className="flex width-full",
        ),
    ],
    className="container mx-auto mt-4",
)

# bg-gray-100

@app.callback(
    Output("heart-rate-graph", "figure"), [Input("heart-rate-update", "n_intervals")]
)
def gen_heart_rate( n ):
    """
    Generate the heart rate graph.

    :params interval: update the graph based on an interval
    """
    global heart_rate
    from engine import export_dataframe
    dfi = export_dataframe()
    heart_rate = (export_heartrate()[0][4]*10)//10
    print(heart_rate)

    trace = dict(
        type="scatter",
        y=dfi["PPG"],
        hoverinfo="skip",
        mode="lines",
    )

    layout = dict(
        height=500,
        xaxis={
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
        State("heart-rate-graph", "figure"),
    ],
)
def gen_wind_histogram( a,b):
    from engine import export_dataframe
    dfi = export_dataframe()

    trace = dict(
        type="scatter",
        y=dfi["GSR"].rolling(window=30).mean(),
        mode="lines",
    )

    layout = dict(
        height=500,
        xaxis={
            "showline": True,
            "zeroline": False,
            "fixedrange": False,
            "title": "Time Elapsed (sec)",
        },
    )

    return dict(data=[trace], layout=layout)

# @app.callback(
#     Output("heart_rate", "figure"),
# )

if __name__ == "__main__":
    app.run_server(debug=True)
