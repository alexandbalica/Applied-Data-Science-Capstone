# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# TASK 1: Add a dropdown list to enable Launch Site selection
dropdown_options = [
    {'label':'All Sites','value':'ALL'},
    {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
    {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
    {'label':'KSC LC-39A','value':'KSC LC-39A'},
    {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}
]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36',
            'font-size': 40}),
    # The default select value is for ALL sites
    html.Div([
        html.Label('Select a Launch Site'),
        dcc.Dropdown(
            id='site-dropdown',
            options=dropdown_options,
            value='ALL',
            placeholder='Select a Launch Site here'
        )
    ]),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10_000,
            step=1_000,
            marks={0: '0',
                2500: '2500',
                5000: '5000',
                7500: '7500',
                10000: '10000'},
            value=[min_payload, max_payload]
        ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    )
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(entered_site):
    df = spacex_df.copy()
    df['outcome'] = df['class'].map({1:'Success', 0:'Failed'})

    if entered_site == 'ALL':
        # Count successes vs failures across all sites

        counts = df['outcome'].value_counts().reset_index()
        counts.columns = ['Outcome','Count']
        fig = px.pie(
            counts,
            names='Outcome',
            values='Count',
            title='Total Launch Outcomes for All Sites'
        )
        return fig
    else:
        # Filter for the selected site and count outcomes

        site_df = df[df['Launch Site'] == entered_site]
        counts = site_df['outcome'].value_counts().reset_index()
        counts.columns = ['Outcome','Count']
        fig = px.pie(
            counts,
            names='Outcome',
            values='Count',
            title=f'Total Launch Outcomes for {entered_site}'
        )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',
        component_property='figure'),
    Input(component_id='site-dropdown',
        component_property='value'),
    Input(component_id="payload-slider",
          component_property='value')
)

def update_scatter(selected_site, payload_range):
    # Filter by payload range

    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]
    
    # Filter by site if not ALL

    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    # Build scatter plot

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=('Correlation between Payload and Success for All Sites'
            if selected_site == 'ALL'
            else f'Correlation between Payload and Success for {selected_site}'),
        labels={'class':'Launch Outcome'}
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
