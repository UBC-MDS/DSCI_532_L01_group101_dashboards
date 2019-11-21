import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os
import pandas as pd


###########################################
# GET DATA
###########################################

df = pd.read_csv("data/Life Expectancy Data.csv")


###########################################
# APP LAYOUT AND APPEARANCE
###########################################

# APP BOILER PLATE
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "UBC Canvas Discussion Board Demo"
port = int(os.environ.get("PORT", 5000))
server = app.server

# COLOURS
colors = {"white": "#ffffff",
          "light_grey": "#d2d7df",
          "ubc_blue": "#082145"
          }

# STYLES
fancy_container = {"border-radius": "5px",
                   "background-color": "#F9F9F9",
                   "margin": "10px",
                   "padding": "15px",
                   "position": "relative",
                   "box-shadow": "2px 2px 2px lightgrey",
                   "border-width": "0"
                   }


# APP LAYOUT
app.layout = html.Div(style={'backgroundColor': colors['light_grey']}, children=[
    # HEADER
    html.Div(className="row", style={'backgroundColor': colors['ubc_blue'], "padding": 10}, children=[
        html.H2('TITLE', style={'color': colors['white']})
    ]),
    # MAIN BODY
    html.Div(className="row", children=[
        # SIDEBAR (left)
        html.Div(className="two columns", style={'padding': 20}, children=[
            html.Img(src="assets/ubc-logo-2.png", width="50")
        ]),
        # MAIN BODY (right)
        html.Div(className="ten columns", style={"backgroundColor": colors['white'], "padding": 20}, children=[
            html.H4("Start a new discussion"),
            html.Label("New topic title:"),
            dcc.Input(id="topic_title", placeholder="Topic Title", type="text", size="75", value=""),
            html.Br(),
            html.Br(),
            html.Label("New message:"),
            dcc.Input(id="topic_message", placeholder="Message Details", type="text", size="75", style={'height': 250}),
            html.Br(),
            html.Br(),
            html.Button('Submit', id='button'),
            html.Hr(),
            html.H5("Existing discussions"),
            html.Div(id="topic_prediction")
        ])
    ])
])

###########################################
# APP CALL BACKS
###########################################

# To be updated

###########################################
# RUN APP
###########################################


if __name__ == '__main__':
    app.run_server(debug=False,
                   host="0.0.0.0",
                   port=port)