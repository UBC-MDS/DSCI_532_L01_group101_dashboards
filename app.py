import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import altair as alt
import numpy as np
import requests
from vega_datasets import data

app = dash.Dash(__name__, assets_folder='assets')
server = app.server


################################
##    Define variable names   ##
################################

# Data Import
data_df = pd.read_csv("./data/WHO_life_expectancy_data_clean.csv")
def get_world_info():
    """Create a dataframe of world info with country information
    
    Returns:
        [pd.DataFrame] -- DataFrame containing a listing of countries and associated information
    """    
    world_info = requests.get("https://restcountries.eu/rest/v2/all")
    world_info_df = pd.DataFrame(world_info.json())
    world_info_df["name"] = world_info_df["name"].str.lower().str.strip()
    world_info_df["numericCode"] = world_info_df["numericCode"].astype(float)
    world_info_df["numericCode"] = world_info_df["numericCode"].fillna(0).astype(int)
    return world_info_df
world_info_df = get_world_info()

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
    ########################### END

    ### Description & Summary Stats
    html.Div(
        [ 
            html.Div(
                    [
                        html.Div( #### H6 id should be referred to sth Else
                            [   html.Div(
                                    [html.H6("Description"), 
                                    html.P("""This dashboard app is created to help decision-makers decide where and what to invest in 
                                               to improve the life expectancy for all. 
                                               Our app will visualize several factors across 193 countries to better understand the global macro trends.""")],
                                    className="pretty_container four columns",
                                ),

                                html.Div(
                                    [html.H6(id="LE_Text"), html.P("Life Expectancy")],
                                    id="lifeExp",
                                    className="pretty_container two columns",
                                ),
                                html.Div(
                                    [html.H6(id="GDP_Text"), html.P("GDP")],
                                    id="GrossDP",
                                    className="pretty_container two columns",
                                ),
                                html.Div(
                                    [html.H6(id="TE_Text"), html.P("Total Expenditure")],
                                    id="TotalExp",
                                    className="pretty_container two columns",
                                ),
                                html.Div(
                                    [html.H6(id="NC_Text"), html.P("Number of Countries")],
                                    id="NumCount",
                                    className="pretty_container two columns",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                    ],
                    className="twelve columns",
            ),
        ]
    ),
    #### End
    html.Br(),

    ########## DASHBOARD
    html.Div(
        [ 
            ############# FILTER part on the Side
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
                        style={"display": "inline-block"},
                        className="dcc_control"
                    ),

                    #### Country Selection Dropdown - STARTS HERE####
                    html.P("Filter by Country Name:", className="control_label"),
                    dcc.Dropdown(
                        id="country_name_selector",
                        options=[{'label':country, 'value':country} for country in countries],
                        value=0,
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
                id="cross-filter-options",
                className="one-third column pretty_container"
            ),

            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph()
                        ]
                    ),
                    
                    html.Br(),

                    html.Div(
                        [
                            dcc.Graph()
                        ]
                    )
                ],
                className="one-third column pretty_container"
            ),

            html.Div(
                [
                    # HEAT MAP
                    html.Div(
                        [
                            html.Iframe(
                                id="heat_map",
                                sandbox='allow-scripts',
                                height='450',
                                width='625',
                                style={'border-width': '0', 'background': 'white'}
                            ),
                            dcc.RadioItems(id="heat_map_colour_selector", value="life_expectancy", options=[
                                {'label': 'Life Expectancy', 'value': 'life_expectancy'},
                                {'label': 'GPD (USD)', 'value': 'gdp'},
                                {'label': 'GDP Log (USD)', 'value': 'gdp_log'},
                        ])
                        ]
                    ),

                    html.Br(),

                    html.Div(
                        [
                            dcc.Graph()
                        ]
                    )
                ],
                className="one-third column pretty_container"
            ),
        ],
    )
    ################## END
])

##############################################
# Call backs
##############################################
@app.callback(
    Output(component_id='heat_map', component_property='srcDoc'),
    [
        Input(component_id='heat_map_colour_selector', component_property='value'),
        Input(component_id='year_slider', component_property='value')
    ]
)
def make_plot_heat_map(colour, year_range=None):
    """Creates an Altair choropleth map
    
    Arguments:
        df {pd.DataFrame} -- Data frame containing the shaded values to plot and country information
        colour {str} -- The column to plot colour scale by (should be either: "life_expectancy", "gdp", or "gdp_log")
        year_range {list} -- List of length 2 containing year range (for example: `[2012, 2015]`) (default: {None}) 
        world_info_df {pd.DataFrame} -- A data frame containing information for each country (default: {world_info_df})
        out {str} -- Either 'df' or 'chart' to determine what object function returns (default: {'chart'})
    
    Returns:
        altair.vegalite.v3.api.Chart -- Altair chart of world map with selected colour scale
            or
        pd.DataFrame -- Data frame used to make chart (useful for trouble shooting missing data)
    """

    # to be turned into arguments eventually...
    df=data_df
    out="chart"
    
    ##################################
    # Clean and tidy data frame
    ##################################
    
    # filter on year range
    if year_range != None:
        df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

    # aggregate and tidy data
    df = (
        df.loc[:, ["country", "status", "life_expectancy", "gdp"]].groupby(["country", "status"])
          .agg("mean")
          .reset_index()
    )
    df["gdp_log"] = np.log(df["gdp"])

    # clean columns for lookup
    df["country"] = df["country"].str.lower().str.strip()

    # clean country names for lookup
    df["country"] = df["country"].str.replace("czechia", "czech republic")
    df["country"] = df["country"].str.replace("democratic people's republic of korea", "korea (democratic people's republic of)") # north korea
    df["country"] = df["country"].str.replace("democratic republic of the congo", "congo (democratic republic of the)")
    df["country"] = df["country"].str.replace("republic of korea", "korea (republic of)") # south korea
    df["country"] = df["country"].str.replace("republic of moldova", "moldova (republic of)")
    df["country"] = df["country"].str.replace("the former yugoslav republic of macedonia", "macedonia (the former yugoslav republic of)")
    df["country"] = df["country"].str.replace("united republic of tanzania", "tanzania, united republic of")


    # look up numeric code from world info
    df = pd.merge(left=df,
                       right=world_info_df[["name", "numericCode"]],
                       left_on="country",
                       right_on="name",
                       how="left").drop("name", 1)

    # numeric code must be string for lookup in altair
    df["numericCode"] = df["numericCode"].astype(str)

    # clean country names for prettier display
    df["country"] = df["country"].str.title()
    
    
    ##################################
    # CREATE PLOT
    ##################################
    
    if colour == "life_expectancy":
        colour_title = "Life Expectancy"
    elif colour == "gdp":
        colour_title = "GDP (USD)"
    elif colour == "gdp_log":
        colour_title = "Log GDP (USD)"
        
    # country plotting data
    countries = alt.topo_feature(data.world_110m.url, 'countries')

    fig = alt.Chart(countries).mark_geoshape(
        fill='#666666',
        stroke='white'
    ).encode(
        alt.Color(colour + ":Q", title = colour_title),
        tooltip=[
            alt.Tooltip("country:N", title="Country"),
            alt.Tooltip("life_expectancy:Q", title="Life Expectancy", format='.2f'),
            alt.Tooltip("gdp:Q", title="GDP (USD)", format="$0,.2f"),
            alt.Tooltip("gdp_log:Q", title="Log GDP (USD)", format="$0,.2f")
        ]
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(df, "numericCode", ["life_expectancy", "country", "gdp", "gdp_log"])
    ).configure_view(
        strokeWidth=0,
    ).project('naturalEarth1')
    
    if out == "chart":
        return fig.to_html()
    else:
        return df

###########
# Run app #
###########

if __name__ == '__main__':
    app.run_server(debug=True)
