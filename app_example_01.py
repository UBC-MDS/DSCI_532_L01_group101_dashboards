import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os
import pandas as pd


###########################################
# GET DATA
###########################################

df = pd.read_csv("data/WHO_life_expectancy_data.csv")


###########################################
# APP LAYOUT AND APPEARANCE
###########################################

# APP BOILER PLATE
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Global Life Expectancy Trends - Dashboard"
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
        html.H2('Global Life Expectancy Trends', style={'color': colors['white']})
    ]),
    # MAIN TOP
    html.Div(className="row", children=[
        html.Div(className="three columns", style=fancy_container, children=[
            html.P("Description")
        ]),
        html.Div(className="three columns", style=fancy_container, children=[
                html.P("Box 1")
        ]),
        html.Div(className="three columns", style=fancy_container, children=[
                html.P("Box 2")
        ])
    ]),
    # MAIN MIDDLE TO BOTTOM
    html.Div(className="row", children=[
        # SIDEBAR FILTERS (left)
        html.Div(className="two columns", style={'padding': 20}, children=[
            dcc.Markdown(style=fancy_container, children=
                """
                # FILTERS
                Time series 1
                """
            ),
            html.Img(src="assets/ubc-logo-2.png", width="50")
        ]),
        # TIME SERIES (middle)
        html.Div(className="four columns", style={"backgroundColor": colors['white'], "padding": 20}, children=[
            dcc.Markdown(style=fancy_container, children=
                """
                # TIME SERIES 1
                Time series 1
                """
            ),
            html.Hr(),
            dcc.Markdown(style=fancy_container, children=
                """
                # TIME SERIES 2
                Time series 2
                """
            ),
        ]),
        # HEAT MAP and DISTRIBUTIONS (right)
        html.Div(className="four columns", style={"backgroundColor": colors['white'], "padding": 20}, children=[
            dcc.Markdown(style=fancy_container, children=
                """
                # HEAT MAP
                Heat map will go here
                """
            ),
            html.Hr(),
            dcc.Markdown(style=fancy_container, children=
                """
                # DISTRIBUTION
                Dist goes here
                """
            )
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
    app.run_server(debug=True,
                   host="0.0.0.0",
                   port=port)