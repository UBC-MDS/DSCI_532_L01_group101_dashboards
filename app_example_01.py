import altair as alt
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import os
import pandas as pd
from dash.dependencies import Input, Output


###########################################
# GET DATA
###########################################

df = pd.read_csv("data/WHO_life_expectancy_data.csv")
df.columns = df.columns.str.strip().str.lower().str.replace("  ", " ").str.replace(" ", "_").str.replace("-", "_")


##############################################
# PLOTS
##############################################



# PLOT 1 - life expectancy over time
def make_plot_01(df, x, y, colour):
    """Create life expectancy by year Altair line plot.
    
    Arguments:
        df {pd.DataFrame} -- Tidy data frame to create plot with
        x {str} -- Specify the column name of the x-axis
        y {str} -- Specify the column name of the y-axis
        colour {str} -- Specify the column name of the line colour
    
    Returns:
        alt.Chart -- Altair chart object
    """    
    # tidy data frame
    selected_cols = [x] + ["life_expectancy"] + [colour]
    df = (
        df[selected_cols]
            .sort_values(by=[colour, x])
            .groupby([colour, x])
            .agg(np.mean)
            .reset_index(drop=False)
    )
    # calculate change in life expectancy
    change_in_life_expectancy = (
        df
        .set_index([x, colour])
        .groupby(colour)
        .pct_change()
        .reset_index(drop=True)
    )
    df["change_in_life_expectancy"] = change_in_life_expectancy.round(2)
    df["life_expectancy"] = df["life_expectancy"].round(2)

    # create chart
    # chart settings based on input
    if y == "life_expectancy":
        y_axis_title = "Life Expectancy"
        y_axis_min = 30
        y_axis_max = 100
        y_axis_step = 2
    else:
        y_axis_title = "Change in Life Expectancy"
        y_axis_min = min(-0.1, df[y].min())
        y_axis_max = max( 0.1, df[y].max())
        y_axis_step = 0.01
    if colour == "status":
        colour_title = "Status"
    else:
        colour_title = "Country"
    
    fig = alt.Chart(
            df
        ).mark_line(
            point=True
        ).encode(
            alt.X(x + ":N", 
                  axis=alt.Axis(labelAngle=0, values=list(range(2000, 2016, 3))), 
                  title="Year"),
            alt.Y(y, 
                  axis=alt.Axis(tickMinStep=y_axis_step),
                  scale=alt.Scale(domain=[y_axis_min, y_axis_max]),
                  title=y_axis_title),
            alt.Color(colour, title=colour.capitalize(), 
                      legend=alt.Legend(values=list(df.sort_values(by=y)[colour].unique()[0:20]))),
            tooltip=[
                alt.Tooltip(colour, title=colour_title),
                alt.Tooltip("life_expectancy", title="Life Expectancy"),
                alt.Tooltip("change_in_life_expectancy", title="Change in Life Expectancy")
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
            html.H6(str(df["life_expectancy"].mean().round(2))),
            html.P("Mean Life Expectancy")
        ]),
        # ROW 2 COLUMN 3
        html.Div(className="pretty_container two columns", children=[
            # mean_gdp = df["gdp"].mean().round(2)
            html.H6("$" + '{:,.2f}'.format(df["gdp"].mean().round(2))),
            html.P("Mean GDP (USD)")
        ]),
        # ROW 2 COLUMN 4
        html.Div(className="pretty_container two columns", children=[
            html.H6(str(df["percentage_expenditure"].mean().round(2))),
            html.P("Mean Health Expenditure (USD)")
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
            dcc.Dropdown(id="dropdown_country", multi=True, options=[{'label': i, 'value': i} for i in df["country"].unique()]),
            html.P(id="dropdown_country_output"),
            html.Br(),
            html.P("Year"),
            dcc.RangeSlider(id="year_slider", min=2000, max=2015, step=1, value=[2000, 2015], marks={i: str(i) for i in range(2000, 2016, 3)}),
            html.Br(),
            html.Br(),
            html.H6("Data Source:"),
            html.A("Kaggle", href="https://www.kaggle.com/kumarajarshi/life-expectancy-who")
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
                        dcc.Markdown("**Select plot y-axis:**"),
                        dcc.RadioItems(id="plot_01_select_y", value="life_expectancy", options=[
                            {'label': 'Life Expectancy', 'value': 'life_expectancy'},
                            {'label': 'Change in Life Expectancy', 'value': 'change_in_life_expectancy'}
                        ])
                    ]),
                    html.Div(className="six columns", children=[
                        dcc.Markdown("**Select plot colour:**"),
                        dcc.RadioItems(id="plot_01_select_colour", value="status", options=[
                            {'label': 'Status', 'value': 'status'},
                            {'label': 'Country', 'value': 'country'}
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
        Input(component_id='plot_01_select_y', component_property='value'),
        Input(component_id='year_slider', component_property='value')
    ]
)
def update_plot_01(country_list, country_status, selected_colour, selected_y, year_range):
    """Update plot 01 in dash app
    
    Arguments:
        country_list {list} -- List of country names to filter on from dropdown_country box
        country_status {str} -- String of country status to filter on from radio buttons
        selected_colour {str} -- Column name to colour lines from radio buttons
        selected_y {str} -- Column name to use for y-axis from radio buttons
        year_range {list} -- List of length 2 containing year range to filter on from year slider (e.g. `[2000, 2005]`)
    
    Returns:
        html file -- Altair chart object as HTML
    """# filter data frame    
    df_filtered = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
    if country_list is None or len(country_list) == 0:
        df_filtered = df_filtered
    else:
        df_filtered = df[df["country"].isin(country_list)]
    if country_status == "All":
        df_filtered = df_filtered
    else:
        df_filtered = df_filtered[df_filtered["status"] == country_status] 

    # adjust colour
    fig = make_plot_01(
        df_filtered, 
        x="year", 
        y=selected_y, 
        colour=selected_colour,
    )
    return fig.to_html()


###########################################
# RUN APP
###########################################


if __name__ == '__main__':
    app.run_server(debug=True,
                   host="0.0.0.0",
                   port=port)