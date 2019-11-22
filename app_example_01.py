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
          "off_white": "#F9F9F9",
          "light_grey": "#d2d7df",
          "ubc_blue": "#082145",
          "yellow": "#FFFF00"
          }

# STYLES
fancy_container = {"border-radius": "5px",
                   "background-color": colors["off_white"],
                   "margin": "10px",
                   "padding": "15px",
                   "position": "relative",
                   "box-shadow": "2px 2px 2px lightgrey",
                   "border-width": "0"
                   }
fancy_container_middle = {"border-radius": "5px",
                    "background-color": colors["off_white"],
                    "margin": "10px",
                    "margin-left": "5px",
                    "padding": "15px",
                    "position": "relative",
                    "box-shadow": "2px 2px 2px lightgrey",
                    "border-width": "0"
                    }
column_style = {"border-radius": "0px",
                #"background-color": colors["yellow"],
                "margin": "0px",
                "padding": "0px",
                "position": "relative",
                "border-width": "0",
               }


# APP LAYOUT
app.layout = html.Div(style={'backgroundColor': colors['light_grey']}, children=[
    # ROW 1 - HEADER
    html.Div(className="row", style={'backgroundColor': colors['ubc_blue'], "padding": 10}, children=[
        html.H2('Global Life Expectancy Trends', style={'color': colors['white']})
    ]),
    # ROW 2 - DESCRIPTION AND BIG NUMBERS
    html.Div(className="row", children=[
        # ROW 2 COLUMN 1
        html.Div(className="pretty_container four columns", style={"margin-left": "10px"}, children=[
            dcc.Markdown(children=
                """
                Dataset related to life expectancy, health factors for 193 countries has been collected from the same WHO 
                data repository website and its corresponding economic data was collected from United Nations.
                """
            )
        ]),
        # ROW 2 COLUMN 2
        html.Div(className="two columns", style=fancy_container_middle, children=[
                html.H6(str(df["Life expectancy "].mean().round(2))),
                html.P("Mean Life Expectancy")
        ]),
        # ROW 2 COLUMN 3
        html.Div(className="two columns", style=fancy_container_middle, children=[
                html.H6(str(df["GDP"].mean().round(2))),
                html.P("Mean GDP")
        ]),
        # ROW 2 COLUMN 4
        html.Div(className="two columns", style=fancy_container_middle, children=[
                html.H6(str(df["percentage expenditure"].mean().round(2))),
                html.P("Mean Health Expenditure")
        ]),
        # ROW 2 COLUMN 4
        html.Div(className="two columns", style=fancy_container_middle, children=[
                html.H6(str(len(df["Country"].unique()))),
                html.P("Number of Countries")
        ])
    ]),
    # ROW 3 - MAIN DASHBOARD
    html.Div(className="row", children=[
        # ROW 3 COLUMN 1 - SIDEBAR FILTERS
        html.Div(className="two columns", style=fancy_container, children=[
            dcc.Markdown(children=
                """
                ### FILTERS
                Time series 1
                """
            )
        ]),
        # ROW 3 COLUMN 2 - TIME SERIES PLOTS
        html.Div(className="five columns", style=column_style, children=[
            dcc.Markdown(style=fancy_container_middle, children=[
                """
                ### TIME SERIES 1
                Time series 1
                """
            ]),
            dcc.Markdown(style=fancy_container_middle, children=[
                """
                ### TIME SERIES 2
                Time series 2
                """
            ]),
        ]),
        # ROW 3 - COLUMN 3 - HEAT MAP and DISTRIBUTIONS
        html.Div(className="five columns", style=column_style, children=[
            dcc.Markdown(style=fancy_container_middle, children=[
                """
                ### HEAT MAP
                Heat map will go here
                """
            ]),
            dcc.Markdown(style=fancy_container_middle, children=[
                """
                ### DISTRIBUTION
                Dist goes here
                """
            ])
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