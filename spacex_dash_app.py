# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_site_names = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[
                                    {
                                        'label':'All Sites',
                                        'value':'ALL'
                                    },
                                    {
                                        'label':'CCAFS LC-40',
                                        'value':'CCAFS LC-40'
                                    },
                                    {
                                        'label':'VAFB SLC-4E',
                                        'value':'VAFB SLC-4E'
                                    },
                                    {
                                        'label':'KSC LC-39A',
                                        'value':'KSC LC-39A'
                                    },
                                     {
                                        'label':'CCAFS SLC-40',
                                        'value':'CCAFS SLC-40'
                                    }
                                ],
                                placeholder='Select a Launch Site here',
                                value='ALL',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0', 2500: '2500', 5000: '5000', 7500:'7500',10000:'10000'},
                                value=[0, 10000]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.groupby(['Launch Site','class']).size().reset_index(name='launch_counts')
    all_sites_successful_counts = filtered_df[filtered_df['class'] == 1]
    if entered_site == 'ALL':
        fig = px.pie(all_sites_successful_counts, values='launch_counts', 
        names='Launch Site', 
        title='Total success launches by site')
        return fig
    else:
        successful = filtered_df['launch_counts'][
            (filtered_df['Launch Site'] == entered_site) &
            (filtered_df['class'] == 1)
            ].values
        failed = filtered_df['launch_counts'][
            (filtered_df['Launch Site'] == entered_site) &
            (filtered_df['class'] == 0)
            ].values
        final = [successful[0], failed[0]]
        fig = px.pie(values=final, 
        names=[1,0], 
        title='Total success launches for site '+entered_site)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value"))
def get_scatter_chart(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        range_data = spacex_df[
            (spacex_df['Payload Mass (kg)'] > payload_slider[0]) &
            (spacex_df['Payload Mass (kg)'] < payload_slider[1])
            ]
        fig = px.scatter(range_data, x='Payload Mass (kg)', y='class',color="Booster Version Category")
        return fig
    else:
        range_as_per_site = range_data[range_data['Launch Site'] == site_dropdown]
        fig = px.scatter(range_as_per_site, x='Payload Mass (kg)', y='class',color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
