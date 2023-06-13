# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(url)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: (Complete) Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site_dropdown',
                                searchable=True,
                                placeholder='Select a Launch Site Here',
                                options=[{'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'site1'},
                                {'label': 'CCAFS SLC-40', 'value': 'site2'},
                                {'label': 'KSC LC-39A', 'value': 'site3'},
                                {'label': 'VAFB SLC-4E', 'value': 'site4'}]),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                html.Br(),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload_slider',
                                min=min_payload, max=10000, step=1000,
                                marks={0:'0 Kg',
                                1000:'1000 Kg',
                                2000:'2000 Kg',
                                3000:'3000 Kg',
                                4000:'4000 Kg',
                                5000:'5000 Kg',
                                6000:'6000 Kg',
                                7000:'7000 Kg',
                                8000:'8000 Kg',
                                9000:'9000 Kg',
                                10000:'10,000 Kg'},
                                value=[min_payload, max_payload]),

                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),

                                html.Div(id="test_div")
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id ='success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site_dropdown', component_property = 'value'))
def update_pie_chart(value):
    select_site = spacex_df
    if value == 'ALL':
        fig = px.pie(select_site[select_site['class'] == 1],
        values='class',
        names='Launch Site',
        title= 'All Launch Sites Success'
        )
        return fig
    else:

        key= {'site1': 'CCAFS LC-40','site2': 'CCAFS SLC-40', 'site3': 'KSC LC-39A', 'site4': 'VAFB SLC-4E'}

        fig = px.pie(select_site[select_site['Launch Site'] == key[value]].groupby('class', as_index=False).count(),
        values= 'Launch Site',
        names='class',
        color= 'class',
        title= f'{key[value]} Launch Site'
        )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output('success-payload-scatter-chart','figure'),
    Input('payload_slider', 'value'),
    Input('site_dropdown','value')
)
def scatter_plot(value_1, value_2):
    data = spacex_df
    payload= data[data['Payload Mass (kg)'] >= value_1[0]]
    payload_range = payload[payload['Payload Mass (kg)']<= value_1[1]]

    if value_2 == 'ALL':
        s_plot = px.scatter(payload_range, x='Payload Mass (kg)', y='class', color='Booster Version')
        return s_plot
    else:
        key= {'site1': 'CCAFS LC-40','site2': 'CCAFS SLC-40', 'site3': 'KSC LC-39A', 'site4': 'VAFB SLC-4E'}
        site_payload = payload_range[payload_range['Launch Site']== key[value_2]]

        s_plot = px.scatter(site_payload, x='Payload Mass (kg)', y='class', color='Booster Version')
        return s_plot



# Run the app
if __name__ == '__main__':
    app.run_server()
