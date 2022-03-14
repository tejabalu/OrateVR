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
app.title = "OrateVR Dashboard"
server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

heart_rate = "N/A";
stress_condition = "N/A";


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
                            html.P("Dashboard displaying speech session information.", className="text-lg text-gray-600"),
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
                            id="heart-rate",
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
                            n_intervals=0,
                        ),
                    ],
                    className="w-full h-full m-4 bg-white shadow-2xl",
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
                    className="w-full h-full m-4 bg-white shadow-2xl",
                ),
            ],
            className="flex flex-col width-full",
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
                                html.H6(id='my-output', className="grow text-[120px] font-medium text-gray-600 block  text-center"),
                                html.H6("Beats per minute", className="grow text-lg font-medium text-gray-600 block text-center"),
                            ]
                        ),
                    ],
                    className="flex flex-col w-1/4 h-full p-4 m-4 bg-white shadow-2xl",
                ),
                html.Div(
                    [
                        html.Div(
                            [html.H6("Stress Condition", className="flex-none h2 py-2 text-2xl text-gray-800")],
                        ),
                        html.Div(
                            [
                                html.H6(id='my-output-stress', className="grow text-[50px] font-medium text-gray-600 block text-center mt-16"),
                            ]
                        ),
                    ],
                    className="flex flex-col w-1/4 h-full p-4 m-4 bg-white shadow-2xl",
                ),
            ],
            className="flex width-full place-content-center h-[20rem] m-4",
        ),
    ],
    className="container mx-auto pb-8 mt-4",
)

# bg-gray-100

@app.callback(
    Output("heart-rate", "figure"), [Input("heart-rate-update", "n_intervals")]
)
def gen_heart_rate( interval ):
    """
    Generate the heart rate graph.

    :params interval: update the graph based on an interval
    """
    global heart_rate
    global stress_condition
    from engine import export_dataframe
    dfi = export_dataframe()
    try:
        heart_rate = (export_heartrate()[0][4]*10)//10
        stress_condition = export_heartrate()[1]
        print(heart_rate, stress_condition)
    except:
        pass


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
        State("heart-rate", "figure"),
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

@app.callback(
    Output(component_id="my-output", component_property="children"),
    [Input("heart-rate-update", "n_intervals")],
)
def update_heartrate_div(interval):
    return heart_rate

@app.callback(
    Output(component_id="my-output-stress", component_property="children"),
    [Input("heart-rate-update", "n_intervals")],
)
def update_stress_condition_div(interval):
    return stress_condition

if __name__ == "__main__":
    app.run_server(debug=True)
