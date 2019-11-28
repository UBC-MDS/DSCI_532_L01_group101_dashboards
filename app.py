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

############################
#     Data wrangling      ##
############################

# Select needed columns
data_df = data_df.iloc[:, [1, 2, 3, 4, 8, 14, 17]]

##add change in percentage columns and formating
data_df['life_pct_change']=data_df.groupby('country').agg(
    {'life_expectancy':'pct_change'})
data_df['gdp_pct_change']=data_df.groupby('country').agg(
    {'gdp':'pct_change'})

def format_num(x, n=4):
    if x is not None:
        return round(x, n)
    
data_df.iloc[:,-2:] = data_df.iloc[:,-2:].apply(format_num)
data_df.iloc[:,-3:-2] = data_df.iloc[:,-3:-2].apply(format_num, args=(1,))

####################################
#      Left two plots functions    #
####################################

def selection(data, y_axis='life_expectancy'):
    '''
    Retun selection layers for interactive plots
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
    
    base = line_chart.encode(
            alt.Y(y_axis))
    
    selector = base.mark_point().encode(
                opacity=alt.condition(nearest, alt.value(1), alt.value(0))
                ).add_selection(nearest)
    
    rules = alt.Chart(data).mark_rule(color='gray').encode(
                x='year:O').transform_filter(nearest)
    
    text = base.mark_text(align='left', dx=5, dy=-5).encode(
                text=alt.condition(nearest, y_axis, alt.value(' '))
                ).transform_filter(nearest)
    
    text_stroke = base.mark_text(align='left', dx=5, dy=-5, 
                                 stroke='white', strokeWidth=3).encode(
                text=y_axis
            ).transform_filter(nearest)
    
    return selector, rules, text, text_stroke

def make_line_plots(country=['Afghanistan'], Yaxis_checked='original'):
    
    #filter country input[list]
    who_df_filter = data_df[data_df.country.isin(country)]
    
    
    line_chart = alt.Chart(who_df_filter).mark_line().encode(
        alt.X('year:O', axis=alt.Axis(labelAngle=0,
                                      title='Year',
                                     values=list(range(2000, 2017, 2)))),
        alt.Color('country')
    ).properties(width=400, height=300)
    
    ##checkbox for original number or change by percentage than last year
    if Yaxis_checked=='original':
        
        #####life expectancy
        life_chart = line_chart.encode(
            alt.Y('life_expectancy', title='Life Expectancy')
        ).properties(title='Life Expectancy Over Time')
        
        selector, rules, text, text_stroke = selection(who_df_filter, 'life_expectancy')
        
        life_chart_inter = alt.layer(life_chart, selector, rules, text_stroke, text)
        
        #####GDP
        gdp_chart = line_chart.encode(
            alt.Y('gdp', title='GDP in USD')
            ).properties(title='GDP in USD Over Time')
        
        selector, rules, text, text_stroke = selection(who_df_filter, 'gdp')
        
        gdp_chart_inter = alt.layer(gdp_chart, selector, rules, text_stroke, text)
            
        return alt.vconcat(life_chart_inter, gdp_chart_inter).configure(background='white')
    
    else:
        ########life expectancy in %
        life_chart = line_chart.encode(
        alt.Y('life_pct_change', title='Change in Percentage',
              axis=alt.Axis(format='%'))
    ).properties(title='Change in Life Expectancy Over Time')
        
        selector, rules, text, text_stroke = selection(who_df_filter, 'life_pct_change')
        
        life_chart_inter = alt.layer(life_chart, selector, rules, text_stroke, text)
        
        #######gdp in %
        gdp_chart = line_chart.encode(
        alt.Y('gdp_pct_change', title='Change in Percentage',
              axis=alt.Axis(format='%'))
        ).properties(title='Change in GDP Over Time')
        
        selector, rules, text, text_stroke = selection(who_df_filter, 'gdp_pct_change')
        
        gdp_chart_inter = alt.layer(gdp_chart, selector, rules, text_stroke, text)
            
        return alt.vconcat(life_chart_inter, gdp_chart_inter).configure(background='white')


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


countries_dict={"Developing":data_df[data_df.status=='Developing'].country.unique(),
               "Developed": data_df[data_df.status=='Developed'].country.unique()}


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
                            {"label": "Developed", "value": "Developed"},
                            {"label": "Developing", "value": "Developing"}
                        ],
                        value="Developed",
                        style={"display": "inline-block"},
                        className="dcc_control"
                    ),

                    #### Country Selection Dropdown - STARTS HERE####
                    html.P("Filter by Country Name:", className="control_label"),
                    dcc.Dropdown(
                        id="country_name_selector",
                       # options=[{'label':country, 'value':country} for country in countries],
                        value=[0],
                        multi=True,
                        className="dcc_control",
                    ),

                    #### Radio button - STARTS HERE####
                    html.P("Line plots Y-axis",className="control_label"),
                    dcc.RadioItems(
                        id="Yaxis_selector",
                    options=[
                        {'label': 'Original number', 'value': 'original'},
                        {'label': 'By Percentage', 'value': 'N'}
                    ],
                    value='original'
                    )  
                ],
                id="cross-filter-options",
                className="one-third column pretty_container"
            ),


            ################line plots####################
            
            html.Div(
                [
                    html.Iframe(
                        sandbox='allow-scripts',
                        id='line-plot',
                        height='900',
                        width='900',
                        style={'border-width': '0'},

                        
                        srcDoc = make_line_plots().to_html()
                    )
                ],
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
        ],
    )
    ################## END
])

#####################
##    callback     ##
#####################

#Chained dropdown for dev/countries
@app.callback(
    Output('country_name_selector', 'options'),
    [Input("country_dev_status_selector", 'value')]
    )
def filter_dev_country(selected_dev):
    return [{'label':i, 'value': i} for i in countries_dict[selected_dev]]


#Line plots inputs callback
@app.callback(
    Output('line-plot', 'srcDoc'),
    [Input('country_name_selector', 'value'),
     Input("Yaxis_selector", 'value')]
    )
def update_line_plots(country, yaxis):
    return make_line_plots(country, yaxis).to_html()


###########
# Run app #
###########

if __name__ == '__main__':
    app.run_server()
