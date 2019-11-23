import altair as alt
import dash
import dash_core_components as dcc
import dash_html_components as html
import janitor
import numpy as np
import os
import pandas as pd
from dash.dependencies import Input, Output


###########################################
# GET DATA
###########################################

df = pd.read_csv("data/WHO_life_expectancy_data.csv")
df = janitor.clean_names(df)

##############################################
# PLOTS
##############################################

# PLOT 1 - life expectancy over time
def df_over_time(df, x, y, colour):
    selected_cols = [x] + [y] + [colour]
    print(selected_cols)
    df = (
        df[selected_cols]
            .groupby([x] + [colour])
            .agg(np.mean)
            .reset_index(drop=False)
    )

    return df

# srcDoc = make_plot().to_hmtl()
def make_plot_01(df, x, y, colour):
    
    # tidy data frame
    selected_cols = [x] + [y] + [colour]
    df = (
        df[selected_cols]
            .groupby([x] + [colour])
            .agg(np.mean)
            .reset_index(drop=False)
    )

    # create chart
    fig = alt.Chart(
            df
        ).mark_line(
            point=True
        ).encode(
            alt.X(x + ":N"),
            alt.Y(y),
            alt.Color(colour),
            tooltip=[
                alt.Tooltip(y, title=y)
            ]
        )

    return fig


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
                """
            )
        ]),
        # ROW 2 COLUMN 2
        html.Div(className="pretty_container two columns", children=[
                html.H6(str(df["life_expectancy_"].mean().round(2))),
                html.P("Mean Life Expectancy")
        ]),
        # ROW 2 COLUMN 3
        html.Div(className="pretty_container two columns", children=[
                html.H6(str(df["gdp"].mean().round(2))),
                html.P("Mean GDP")
        ]),
        # ROW 2 COLUMN 4
        html.Div(className="pretty_container two columns", children=[
                html.H6(str(df["percentage_expenditure"].mean().round(2))),
                html.P("Mean Health Expenditure")
        ]),
        # ROW 2 COLUMN 4
        html.Div(className="pretty_container two columns", children=[
                html.H6(str(len(df["country"].unique()))),
                html.P("Number of Countries")
        ])
    ]),
    # ROW 3 - MAIN DASHBOARD
    html.Div(className="row", children=[
        # ROW 3 COLUMN 1 - SIDEBAR FILTERS
        html.Div(className="pretty_container two columns", style={"margin-left": "10px"}, children=[
            html.H6("Filters"),
            html.P("Country Status"),
            dcc.RadioItems(id="radio_country_status", options=[
                {'label': 'Developed', 'value': 'Developed'},
                {'label': 'Un-developed', 'value': 'Un-developed'}
            ]),
            html.Br(),
            html.P("Country"),
            dcc.Dropdown(id="dropdown_country", multi=True, options=[
                {'label': 'Canada', 'value': 'Canada'},
                {'label': 'USA', 'value': 'USA'},
                {'label': 'Mexico', 'value': 'Mexico'}
            ]),
            html.Br(),
            html.P("Year"),
            dcc.Slider(id="year_slider", min=2010, max=2015, step=1)
        ]),
        # ROW 3 COLUMN 2 - TIME SERIES PLOTS
        html.Div(className="five columns", style=column_style, children=[
            html.Div(className="pretty_container", children=[
                dcc.Markdown(
                    """
                    ###### Life expectancy over time
                    """
                ),
                html.Iframe(
                    id="plot_01",
                    sandbox='allow-scripts',
                    height='450',
                    width='625',
                    style={'border-width': '0'},
                    srcDoc=make_plot_01(df, "year", "life_expectancy_", "status").to_html()
                )
            ]),
            dcc.Markdown(className="pretty_container", children=[
                """
                ### TIME SERIES 2
                Time series 2
                """
            ]),
        ]),
        # ROW 3 - COLUMN 3 - HEAT MAP and DISTRIBUTIONS
        html.Div(className="five columns", style=column_style, children=[
            dcc.Markdown(className="pretty_container", children=[
                """
                ### HEAT MAP
                Heat map will go here
                """
            ]),
            dcc.Markdown(className="pretty_container", children=[
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