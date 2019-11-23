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
def make_plot_01(df, x, y, colour):
    
    # tidy data frame
    selected_cols = ["year"] + ["life_expectancy_"] + [colour]
    df = (
        df[selected_cols]
            .sort_values(by=[colour, "year"])
            .groupby([colour, "year"])
            .agg(np.mean)
            .reset_index(drop=False)
    )

    # calculate change in life expectancy
    change_in_life_expectancy = (
        df
        .set_index(["year", colour])
        .groupby(colour)
        .pct_change()
        .reset_index(drop=True)
    )
    df["change_in_life_expectancy_"] = change_in_life_expectancy.round(2)

    # create chart
    
    fig = alt.Chart(
            df
        ).mark_line(
            point=True
        ).encode(
            alt.X(x + ":N", axis=alt.Axis(labelAngle=45)),
            alt.Y(y, axis=alt.Axis(tickMinStep=0.01)),
            alt.Color(colour),
            tooltip=[
                alt.Tooltip("life_expectancy_", title="Life Expectancy"),
                alt.Tooltip("change_in_life_expectancy_", title="Change in Life Expectancy")
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
            dcc.RadioItems(id="radio_country_status", value="All", options=[
                {'label': "All", 'value': "All"},
                {'label': 'Developed', 'value': 'Developed'},
                {'label': 'Developing', 'value': 'Developing'}
            ]),
            html.Br(),
            html.P("Country"),
            dcc.Dropdown(id="dropdown_country", value=None, multi=True, options=[{'label': i, 'value': i} for i in df["country"].unique()]),
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
                    style={'border-width': '0'}
                ),
                html.Div(className="row", children=[
                    html.Div(className="six columns", children=[
                        dcc.Markdown("**Select plot colour:**"),
                        dcc.RadioItems(id="plot_01_select_colour", value="status", options=[
                            {'label': 'Status', 'value': 'status'},
                            {'label': 'Country', 'value': 'country'}
                        ])
                    ]),
                    html.Div(className="six columns", children=[
                        dcc.Markdown("**Select plot y-axis:**"),
                        dcc.RadioItems(id="plot_01_select_y", value="life_expectancy_", options=[
                            {'label': 'Life Expectancy', 'value': 'life_expectancy_'},
                            {'label': 'Change in Life Expectancy', 'value': 'change_in_life_expectancy_'}
                        ])
                    ])
                ])
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

#################
# Plot 1
#################
@app.callback(
    Output(component_id='plot_01', component_property='srcDoc'),
    [
        Input(component_id='dropdown_country', component_property='value'),
        Input(component_id='radio_country_status', component_property='value'),
        Input(component_id='plot_01_select_colour', component_property='value'),
        Input(component_id='plot_01_select_y', component_property='value') # plot_01_select_y
    ]
)
def update_plot_01(country_list, country_status, selected_colour, selected_y):
    # filter data frame
    if country_list is None:
        df_filtered = df
    else:
        df_filtered = df[df["country"].isin(country_list)]
    if country_status == "All":
        df_filtered = df_filtered
    else:
        df_filtered = df_filtered[df_filtered["status"] == country_status] 
    # TODO - when country dropdown is nothing, there is an error. need an if statement for this...

    # adjust colour
    fig = make_plot_01(
        df_filtered, 
        x="year", 
        y=selected_y, 
        colour=selected_colour
    )
    return fig.to_html()


###########################################
# RUN APP
###########################################


if __name__ == '__main__':
    app.run_server(debug=True,
                   host="0.0.0.0",
                   port=port)