import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import altair as alt
import numpy as np
import requests
from vega_datasets import data

################################
# General app settings
################################

app = dash.Dash(__name__, assets_folder='assets')
app.title = 'World Life Expectancy Dashboard App'
server = app.server


################################
# DATA
################################

# Load life expectancy data
data_df = pd.read_csv("data/WHO_life_expectancy_data_clean.csv")

# Load additional country information
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



def make_line_plot_df(df):
    """Wrangle data for line plots
    
    Arguments:
        df {pd.DataFrame} -- Raw life expectancy data frame
    
    Returns:
        pd.DataFrame -- In format wrangled for line plots
    """    
    
    df

    # Select needed columns
    df = df.loc[:, ["country", "year", "status", "life_expectancy", "gdp"]]
    

    ##add change in percentage columns and formating
    df['life_pct_change']=df.groupby('country').agg(
        {'life_expectancy':'pct_change'})
    df['gdp_pct_change']=df.groupby('country').agg(
        {'gdp':'pct_change'})
    
    def format_num(x, n=4):
        """
        Round number to n decimal place filtering None component

        Arguments:
        x (pd.DataFrame or pd.Series)
        """
        if x is not None:
            return round(x, n)
        
    df.loc[:, ['life_pct_change', 'gdp_pct_change']] = df.loc[:, ['life_pct_change', 'gdp_pct_change']].apply(format_num)
    df.loc[:,'gdp'] = df.loc[:, 'gdp'].apply(format_num, args=(1,))

    return df

################################
# Line plots
################################

def selection(data, y_axis='life_expectancy'):
    
    '''
    Create layers for interactive line selection

    Arguments:
    df {pd.DataFrame} -- life expectancy data frame
    y_axis (str): column name for y axis
    
    Returns:
    selection layers of conditional input and output
    '''
    nearest = alt.selection_single(encodings=['x'], 
                                   on='mouseover',  
                                   nearest=True,    
                                   empty='none')
    
    line_chart = alt.Chart(data).mark_line().encode(
        alt.X('year:O', axis=alt.Axis(labelAngle=0,
                                      title='Year',
                                      values=list(range(2000, 2017, 2)))),
        alt.Color('country')
    ).properties(width=400, height=300)

    #crease base plot with specified y-axis 
    base = line_chart.encode(
            alt.Y(y_axis))
    
    #selector points
    selector = base.mark_point().encode(
                opacity=alt.condition(nearest, alt.value(1), alt.value(0))
                ).add_selection(nearest)
    
    #transformed rule line based on selector
    rules = alt.Chart(data).mark_rule(color='gray').encode(
                x='year:O').transform_filter(nearest)

    #transformed text based on selector
    text = base.mark_text(align='left', dx=5, dy=-5).encode(
                text=alt.condition(nearest, y_axis, alt.value(' '))
                ).transform_filter(nearest)

    #transformed white text as text background based on selector
    text_stroke = base.mark_text(align='left', dx=5, dy=-5, 
                                 stroke='white', strokeWidth=3).encode(
                text=y_axis
            ).transform_filter(nearest)
    
    return selector, rules, text, text_stroke

def make_line_plots(data_df=data_df, country=['Afghanistan'], Yaxis_checked='original'):

    """
    Arguments:
        df {pd.DataFrame} -- Life expectancy data frame
        country {list} -- The column to plot colour scale by (should be either: "life_expectancy", "gdp", or "gdp_log")
        Yaxis_checked {str} -- only for str either 'original' or 'change_in_percent' 
        
    
    Returns:
        two altair line charts in a column
    """
    
    data_df_line_plot = make_line_plot_df(data_df)

    #filter country input[list]
    who_df_filter = data_df_line_plot[data_df_line_plot["country"].isin(list(country))]
    
    
    line_chart = alt.Chart(who_df_filter).mark_line().encode(
        alt.X('year:O', axis=alt.Axis(labelAngle=0,
                                      title='Year',
                                     values=list(range(2000, 2017, 2)))),
        alt.Color('country')
    ).properties(width=400, height=300)
    
    ##checkbox for original number or change by percentage than last year
    if Yaxis_checked == 'original':
        #####life expectancy
        life_chart = line_chart.encode(
            alt.Y('life_expectancy:Q', title='Life Expectancy')
        ).properties(title='Life Expectancy Over Time').interactive()
        
        selector, rules, text, text_stroke = selection(who_df_filter, 'life_expectancy')
        
        life_chart_inter = alt.layer(life_chart, selector, rules, text_stroke, text)
        
        #####GDP
        gdp_chart = line_chart.encode(
            alt.Y('gdp:Q', title='GDP in USD')
        ).properties(title='GDP in USD Over Time').interactive()
        
        selector, rules, text, text_stroke = selection(who_df_filter, 'gdp')
        
        gdp_chart_inter = alt.layer(gdp_chart, selector, rules, text_stroke, text)
            
        return alt.vconcat(life_chart_inter, gdp_chart_inter
                           ).configure(background='white').configure_axis(grid=False)
    
    elif Yaxis_checked == "change_in_percent":
        ########life expectancy in %
        life_chart = line_chart.encode(
            alt.Y('life_pct_change:Q', title='Change in Percentage',
                   axis=alt.Axis(format='%'))
        ).properties(title='Change in Life Expectancy Over Time').interactive()
        
        selector, rules, text, text_stroke = selection(who_df_filter, 'life_pct_change')
        
        life_chart_inter = alt.layer(life_chart, selector, rules, text_stroke, text)
        
        #######gdp in %
        gdp_chart = line_chart.encode(
        alt.Y('gdp_pct_change:Q', title='Change in Percentage',
              axis=alt.Axis(format='%'))
        ).properties(title='Change in GDP Over Time').interactive()
        
        selector, rules, text, text_stroke = selection(who_df_filter, 'gdp_pct_change')
        
        gdp_chart_inter = alt.layer(gdp_chart, selector, rules, text_stroke, text)
            
        return alt.vconcat(life_chart_inter, gdp_chart_inter
                           ).configure(background='white').configure_axis(grid=False)


##############################################
# Heat map
##############################################
def make_heat_map(df=data_df, colour="life_expectancy", year_range=None):
    """Creates an Altair choropleth map
    
    Arguments:
        df {pd.DataFrame} -- Data frame containing the shaded values to plot and country information
        colour {str} -- The column to plot colour scale by (should be either: "life_expectancy", "gdp", or "gdp_log")
        year_range {list} -- List of length 2 containing year range (for example: `[2012, 2015]`) (default: {None}) 
        
    
    Returns:
        altair.vegalite.v3.api.Chart -- Altair chart of world map with selected colour scale
    """
    
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
        title = "World Heat Map - Mean Life Expectancy"
    elif colour == "gdp":
        colour_title = "GDP (USD)"
        title = "World Heat Map - Mean GDP (USD)"
    elif colour == "gdp_log":
        colour_title = "Log GDP (USD)"
        title = "World Heat Map - Mean Log GDP (USD)"
        
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
    ).properties(
        title=title,
        width=400, 
        height=300
    ).project('naturalEarth1')
    
    return fig

##############################################
# Life vs. GDP
##############################################
def make_gdp_vs_life_scatter(df, x, colour, year_range=None):
    """Creates an Altair scatter plot
    
    Arguments:
        df {pd.DataFrame} -- Data frame containing the shaded values to plot and country information
        x {str} -- The column to plot the x axis on (should be either: "gdp", or "gdp_log")
        colour {str} -- The column to plot point colour by (should be either: "status", or "country")
        year_range {list} -- List of length 2 containing year range (for example: `[2012, 2015]`) (default: {None}) 
    
    Returns:
        altair.vegalite.v3.api.Chart
    """
    
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
    
    ##################################
    # CREATE PLOT
    ##################################

    # create plot
    if x == "gdp":
        x_title = "GDP (USD)"
        title = "Life Expectancy vs. Mean GDP (USD)"
    else:
        x_title = "GDP log (USD)"
        title = "Life Expectancy vs. Mean Log GDP (USD)"
    if colour == "status":
        colour_title = "Status"
    else:
        colour_title = "Country"
        
    fig = alt.Chart(df).mark_point(
        opacity=1/2
    ).encode(
        alt.X(x + ":Q", title=x_title),
        alt.Y("life_expectancy:Q", bin=alt.Bin(step=2), title="Life Expectancy"),
        alt.Color(colour + ":N", title=colour_title),
        tooltip=[
                alt.Tooltip("country", title="Country"),
                alt.Tooltip("status", title="Status"),
                alt.Tooltip("gdp:Q", title="GDP (USD)", format="$0,.2f"),
                alt.Tooltip("gdp_log:Q", title="GDP log (USD)", format="$0,.2f")
            ]
    ).properties(
        title=title,
        width=400, 
        height=300
    )
    
    return fig

################################
# Filter setup
################################
##  - Create Control Buttons  ##
################################

# Define variables to for filters
dev_status = list(data_df["status"].unique())
countries = list(data_df["country"].unique())
years = list(data_df["year"].unique())

country_status_options = [
    {"label":dev_stat , "value": dev_stat} for dev_stat in dev_status
]

country_name_options = [
    {"label": country , "value": country} for country in countries
]

year_options = [
    {"label": year, "value": year} for year in years
]

countries_dict={"Developing":data_df[data_df.status=='Developing'].country.unique(),
               "Developed": data_df[data_df.status=='Developed'].country.unique()}


##############################################
# App layout
##############################################

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
                        html.Div(
                            [   html.Div(
                                    [html.H6("Description"), 
                                    html.P("""This dashboard app is created to help decision-makers decide where and what to invest in 
                                               to improve the life expectancy for all. 
                                               Our app will visualize several factors across 193 countries to better understand the global macro trends.""")],
                                    className="pretty_container four columns",
                                ),

                                html.Div(
                                    [html.H6(str(round(data_df["life_expectancy"].mean(), 2))), 
                                    html.P("Mean Life Expectancy")],
                                    id="lifeExp",
                                    className="pretty_container two columns",
                                ),
                                html.Div(
                                    [html.H6("$" + '{:,.2f}'.format(round(data_df["gdp"].mean(),2))), 
                                    html.P("Mean GDP (USD)")],
                                    id="GrossDP",
                                    className="pretty_container two columns",
                                ),
                                html.Div(
                                    [html.H6("$" + '{:,.2f}'.format(round(data_df["gdp"].std(),2))), 
                                    html.P("Standard Deviation GDP (USD)")],
                                    id="GrossDPsd",
                                    className="pretty_container two columns",
                                ),
                                html.Div(
                                    [html.H6(str(len(data_df["country"].unique()))), 
                                    html.P("Number of Countries")],
                                    id="NumCount",
                                    className="pretty_container two columns",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                    ],
                    className="row1 twelve columns",
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
                    #### Country Selection Dropdown - STARTS HERE####
                    html.P("Filter by Country Name:", className="control_label"),
                    dcc.Dropdown(
                        id="country_name_selector",
                       options=[{'label':country, 'value':country} for country in countries],
                        value=["Mexico", "Turkey"],
                        multi=True,
                        className="dcc_control",
                    ),
                    #### Status Radio Button - STARTS HERE####
                    html.P("Filter drop down menu by Country Status:", className="control_label"),
                    dcc.RadioItems(
                        id="country_dev_status_selector",
                        options=[
                            {"label": "Developed", "value": "Developed"},
                            {"label": "Developing", "value": "Developing"}
                        ],
                        value="Developed",
                        style={"display": "inline-block"},
                        className="dcc_control"
                    ),

                    html.Br(),
                    html.Br(),

                ],
                id="cross-filter-options",
                className="column pretty_container",
                style={"width":"25%","display":"inline","border-width":"0", "vertical-align":"top"},
            ),

            ################line plots####################
            
            html.Div(
                [
                    # Line plots
                    html.Iframe(
                        sandbox='allow-scripts',
                        id='line-plot',
                        height='800',
                        width='100%',
                        style={'border-width': '0'},
                    ),
                    #### Yaxis Change Radio button - STARTS HERE####
                    html.P("Select line plot y-axis:",className="control_label"),
                    dcc.RadioItems(
                        id="Yaxis_selector",
                        options=[
                            {'label': 'Original number', 'value': 'original'},
                            {'label': 'Change in Percentage', 'value': 'change_in_percent'}
                        ],
                        value='original'
                    )
                ],
                className="column2 pretty_container",
                style={"width":"33%", "display":"inline-block","border":"0", "vertical-align":"top"},
            ),
            
            html.Div(
                [
                    # HEAT MAP
                    
                    html.Iframe(
                        id="heat_map",
                        sandbox='allow-scripts',
                        height='350',
                        width='100%',
                        style={'border-width': '0', 'background': 'white'}
                    ),
                    html.P("Select fill colour for heat map:"),
                    dcc.RadioItems(id="heat_map_colour_selector", value="life_expectancy", options=[
                        {'label': 'Life Expectancy', 'value': 'life_expectancy'},
                        {'label': 'GPD (USD)', 'value': 'gdp'},
                        {'label': 'GDP Log (USD)', 'value': 'gdp_log'}]
                    ),
                        
                    html.Br(),

                    html.Iframe(
                        id="gdp_vs_life_scatter",
                        sandbox='allow-scripts',
                        height='400',
                        width='100%',
                        style={'border-width': '0', 'background': 'white'}
                    ),
                    html.Div([
                                html.Div([
                                    html.P("Select point colour:"),
                                    dcc.RadioItems(id="gdp_vs_life_scatter_colour", value="status", options=[
                                        {'label': 'Status', 'value': 'status'},
                                        {'label': 'Country', 'value': 'country'}]
                                    )
                                ], className="six columns"),
                                html.Div([
                                    html.P("Select x-axis:"),
                                    dcc.RadioItems(id="gdp_vs_life_scatter_x", value="gdp", options=[
                                        {'label': 'GPD (USD)', 'value': 'gdp'},
                                        {'label': 'GDP Log (USD)', 'value': 'gdp_log'}]
                                    )
                                ], className="six columns")
                            ], className="row"),
                        html.Br(),
                        html.Div([
                            #### Year Range Slider - STARTS HERE####
                            html.P("Select year range:"),
                            dcc.RangeSlider(id="year_slider", min=2000, max=2015, step=1, value=[2000, 2015], 
                                            marks={i: str(i) for i in range(2000, 2016, 3)}),
                    
                        ]),
                        html.Br(),
                        html.Br()      
                ],
                className="column3 pretty_container",
                style={"width":"33%","display":"inline-block", "border-width":"0","vertical-align":"top"}
            ),
        ],
        className="row2 twelve columns"
    )
    ################## END
])

##############################################
# Call backs
##############################################


#Line plots inputs callback
@app.callback(
    Output('line-plot', 'srcDoc'),
    [Input('country_name_selector', 'value'),
     Input("Yaxis_selector", 'value')]
    )
def update_line_plots(country, yaxis):
    """Update line plot
    
    Arguments:
        country {list} -- List of countries to filter on
        yaxis {str} -- Determine which column should be on plot y axis
    
    Returns:
        html -- Altair chart in html
    """    
    return make_line_plots(country=country, Yaxis_checked=yaxis).to_html()

# HEATMAP
@app.callback(
    Output(component_id='heat_map', component_property='srcDoc'),
    [
        Input(component_id='heat_map_colour_selector', component_property='value'),
        Input(component_id='year_slider', component_property='value')
    ]
)
def update_heat_map(selected_colour, year_range):
    """Update heat map in dash
    
    Arguments:
        selected_colour {str} -- Column name to use for map colouring
        year_range {list} -- List of length 2 with start and end year (e.g. [2000, 2015])
    
    Returns:
        html -- Altair chart in html
    """    
    return make_heat_map(colour=selected_colour, year_range=year_range).to_html()


# Scatter plot
@app.callback(
    Output(component_id='gdp_vs_life_scatter', component_property='srcDoc'),
    [
        Input(component_id='gdp_vs_life_scatter_x', component_property='value'),
        Input(component_id='gdp_vs_life_scatter_colour', component_property='value'),
        Input(component_id='year_slider', component_property='value')
    ]
)
def update_gdp_vs_life_scatter(selected_x, selected_colour, year_range): 
    """Update gdp vs. life expectancy scatter plot
    
    Arguments:
        selected_x {str} -- Name of column for x-axis
        selected_colour {str} -- Name of column to generate point colour
        year_range {list} -- List of length two containing year range (e.g. [2011, 2013])
    
    Returns:
        html -- Altair chart in html
    """    
    return make_gdp_vs_life_scatter(df=data_df, 
                                    x=selected_x, 
                                    colour=selected_colour, 
                                    year_range=year_range).to_html()



#Chained dropdown for dev/countries
@app.callback(
    Output('country_name_selector', 'options'),
    [Input("country_dev_status_selector", 'value')]
    )
def filter_dev_country(selected_dev):   
    """Update country drop down filter
    
    Arguments:
        selected_dev {str} -- Determine if dropdown should show developed or developing countries

    Returns:
        html -- Altair chart in html
    """     
    return [{'label':i, 'value': i} for i in countries_dict[selected_dev]]


##############################################
# Run app
##############################################

if __name__ == '__main__':
    app.run_server(debug=True)
