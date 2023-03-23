import pandas as pd
import numpy as np
import time
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.long_callback import CeleryLongCallbackManager
from dash.dependencies import Input, Output, State
from celery import Celery
import plotly.graph_objects as go
import plotly.express as px

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="A Figure Displayed with fig.show()"
)

celery_app = Celery(
    __name__, broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0", backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/1"
)
long_callback_manager = CeleryLongCallbackManager(celery_app)

app = dash.Dash(__name__, 
                long_callback_manager=long_callback_manager,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

modal = html.Div(
    [
        dbc.Button("Open modal", id="open", n_clicks=0, style={'display': 'none'}),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Alert")),
                dbc.ModalBody("Task is done running"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
            keyboard=False,
            backdrop="static",
        ),
    ]
)

app.layout = html.Div(
    [
        html.Div([html.P(id="paragraph_id", children=["Button not clicked"])]),
        html.Button(id="button_id", children="Run Job!"),
        html.Button(id="cancel_button_id", children="Cancel Running Job!"),
        html.Div([html.P(id="paragraph_id2", children=["Button not clicked"])]),
        html.Button(id="button_id2", children="Run longer Job2!"),
        modal,
        dcc.Graph(id="plot", figure=fig)
    ]
)

@app.callback(
    Output("modal", "is_open", allow_duplicate=True),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
    prevent_initial_call=True
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.long_callback(
    output=[
        Output("paragraph_id", "children"),
        Output("modal", "is_open")
    ],
    inputs=Input("button_id", "n_clicks"),
    running=[
        (Output("button_id", "disabled"), True, False),
        (Output("cancel_button_id", "disabled"), False, True),
    ],
    cancel=[Input("cancel_button_id", "n_clicks")],
    state=[State("modal", "is_open")],
    prevent_initial_call=True
)
def callback(n_clicks, is_open):
    time.sleep(2.0)
    return [f"Clicked {n_clicks} times"], not is_open


@app.long_callback(
    output=[
        Output("paragraph_id2", "children"),
        Output('plot', 'figure')
    ],
    inputs=Input("button_id2", "n_clicks"),
    running=[
        (Output("button_id2", "disabled"), True, False),
    ],
    prevent_initial_call=True
)
def callback2(n_clicks):
    df= pd.read_csv('ElectricCarData_Clean.csv')
    
    if int(n_clicks) % 2 == 0:
        a = np.arange(1,104)
        fig = px.bar(df, x='Brand',y=a)
    else:
        fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns),
        cells=dict(values=[df[c] for c in df.columns])
    )])
    
    return [f"Clicked {n_clicks} times"], fig

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True)