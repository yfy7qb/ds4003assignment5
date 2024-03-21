
# import libraries
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

# Read in and sort data
df = pd.read_csv('gdp_pcap.csv')
df = df.sort_values('country').reset_index(drop = True)

# Set column headers to integers
for j in range (1,302):
    df.columns.values[j] = int(df.columns.values[j])

# Define years
min_year = list(df.columns.values)[1] # 1800 in this dataset
max_year = list(df.columns.values)[-1] # 2100 in this dataset

# Clean data
for i in range (0,195): # country range
    for j in range (1,302): # year range
        if str(df.iloc[i,j]).endswith('k'): # if number is X.Xk
            df.iloc[i,j] = 1000*float(df.iloc[i,j][:-1])
        else:
            df.iloc[i,j] = float(df.iloc[i,j])

# Transpose dataset in order to prep new dataframe
dfT = df.T # Transposition
dfT.columns = dfT.iloc[0] # Set column headers to country names
dfT = dfT.iloc[1: , :] # Drop country names

# Pre-allocate alternative dataframe to populate graph
dfnew = pd.DataFrame(0, index=np.arange(301*195), columns=['Year','Country','GDP per Capita']) # Data frame of all zeros

for i in range(0,195): # Across country range
    for j in range(0,301): # Across year range
        row = 301*i+j
        dfnew.iloc[row,0] = dfT.index[j] # Year value
        dfnew.iloc[row,1] = dfT.columns[i] # Country value
        dfnew.iloc[row,2] = dfT.iloc[j,i] # GDP per capita value

# Add in stylesheet
stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Set up app and sever
app = Dash(__name__, external_stylesheets=stylesheet)
server = app.server

# Set app layout
app.layout = html.Div([
    
    # Adding title
    html.Div(html.H1(children = 'Graph of GDP per capita')),

    # Adding description
    html.Div(html.P(children =
        "This app takes a dropdown of country options and a slider of years and create a graph of those countries' GDP per capita across the specified year range. This app is the same as Assignment 4; however, it has been updated to fix the issues with the slider as well as be interactive. Data can be changed by adjusting the dropdown and slider."
        )),

    # Adding dropdown
    html.Div(dcc.Dropdown(
            id = 'dropdown',
            options = dfT.columns,
            value =  [],
            multi = True,
            className="six columns"
            )),

    # Adding slider
    html.Div(dcc.RangeSlider(
        id='slider',
        min = min_year,
        max = max_year,
        step = 1,
        value = [min_year,max_year],
        marks = {i: '{}'.format(i) for i in range(min_year, max_year + 50, 50)},
        className="six columns"
    ), className = 'row'),

    # Add space
    html.Hr(),

    # Adding graph
    html.Div(dcc.Graph(id = 'gdpfig'))
    ])

# Define callback function
@callback(
    Output('gdpfig', 'figure'),
    Input('slider', 'value'),
    Input('dropdown', 'value'))
# Define update function
def update_graph(slider, dropdown):

    # Filter for data within range of slider
    dff = dfnew[dfnew['Year'] >= slider[0]][dfnew['Year'] <= slider[1]]

    # Filter for countries in dropdown (if no countries, skips if and shows all)
    if dropdown:
        dff = dff[dff['Country'].isin(dropdown)]

    # Define figure
    fig = px.line(dff, 
                      x = 'Year', 
                      y = 'GDP per Capita',
                      color = 'Country',
                      title = 'Basic Line Chart with Color Encoding')

    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug = True)


