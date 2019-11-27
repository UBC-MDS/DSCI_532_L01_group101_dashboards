import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import altair as alt
import numpy as np

app = dash.Dash(__name__, assets_folder='assets')
server = app.server


################################
##    Define variable names   ##
################################

# Data Import
data_df = pd.read_csv("./data/WHO_life_expectancy_data_clean.csv")

# Define variables to use
dev_status = list(data_df["status"].unique())
countries = list(data_df["country"].unique())
years = list(data_df["year"].unique())


################################
## Filter Options on the Left ##
##  - Create Control Buttons  ##
################################

country_status_options = [
    {"label":dev_stat , "value": dev_stat} for dev_stat in dev_status
]

country_name_options = [
    {"label": country , "value": country} for country in countries
]

year_options = [
    {"label": year, "value": year} for year in years
]


# Title
app.title = 'World Life Expectancy Dashboard App'


############################################
#########           Layout        ##########
############################################

app.layout = html.Div([

    #### The Top Header Part
    html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("ubc-mds.png"),
                            id="UBC-MDS",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Global Life Expectancy Trends",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Overview of Inequality of Life Expectancy", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Original Data", id="raw_data"),
                            href="https://www.kaggle.com/kumarajarshi/life-expectancy-who/data",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),

    ### FILTERS On Side
        html.Div(
            [
                html.Div(
                    [
                        #### Status Radio Button - STARTS HERE####
                        html.P("Filter by Country Status:", className="control_label"),
                        dcc.RadioItems(
                            id="country_dev_status_selector",
                            options=[
                                {"label": "Developed", "value": 0},
                                {"label": "Developing", "value": 1}
                            ],
                            value="Developed",
                            #labelStyle={"display": "inline-block"},
                            className="dcc_control"
                        ),

                        #### Country Selection Dropdown - STARTS HERE####
                        html.P("Filter by Country Name:", className="control_label"),
                        dcc.Dropdown(
                            id="country_name_selector",
                            options=[{'label':country, 'value':country} for country in countries],
                            value=0,
                            #labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),

                        #### Year Filter Range Bar - STARTS HERE####
                        html.P("Filter by year:",className="control_label"),
                        dcc.RangeSlider(
                            id="year_slider",
                            min= np.min(years),
                            max= np.max(years),
                            step= 1,
                            marks={i:"{}".format(i) for i in range(np.min(years),np.max(years)+1)},
                            value=[np.min(years), np.max(years)],
                            className="dcc_control",
                        )
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
            ])
])



###########
# Run app #
###########

if __name__ == '__main__':
    app.run_server()
