import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # TASK 1: Launch Site Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [
            {'label': site, 'value': site}
            for site in spacex_df['Launch Site'].unique()
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie Chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[0, 10000],
        marks={i: str(i) for i in range(0, 10001, 2500)}
    ),

    html.Br(),

    # TASK 4: Scatter Chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for Pie Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Success vs Failure for site {entered_site}'
        )
        return fig

# TASK 4: Callback for Scatter Plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_plot(entered_site, payload_range):
    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload Mass vs Launch Outcome'
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run()
