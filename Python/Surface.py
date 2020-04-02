import plotly.graph_objects as go
from plotly.subplots import make_subplots
import Pricing_Product as pp

import numpy as np


# Initialize figure with 4 3D subplots
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{'type': 'surface'}, {'type': 'surface'}],
           [{'type': 'surface'}, {'type': 'surface'}]],
    subplot_titles=("Delta", "Gamma", "Vega", "Theta"))

# Generate data
spot = 100

x = list()
y = list()
z = list()

for i in range(1,20):
    x.append(spot*(0.5 + 0.05*i))
    y.append(i/5)

xGrid, yGrid = np.meshgrid(y, x)
z = pp.Delta(spot,yGrid,xGrid,0.01,0.2)

# adding surfaces to subplots.
fig.add_trace(
    go.Surface(x=x, y=y, z=z, colorscale='Delta',name='Delta', showscale=False),
    row=1, col=1)

z= pp.Gamma(spot,yGrid,xGrid,0.01,0.2)

fig.add_trace(
    go.Surface(x=x, y=y, z=z, colorscale='Delta',name='Gamma', showscale=False),
    row=1, col=2)

z = pp.Vega(spot,yGrid,xGrid,0.01,0.2)

fig.add_trace(
    go.Surface(x=x, y=y, z=z, colorscale='Delta',name='Vega', showscale=False),
    row=2, col=1)

z = pp.Tetha(spot,yGrid,xGrid,0.01,0.2)

fig.add_trace(
    go.Surface(x=x, y=y, z=z, colorscale='Delta',name='Theta', showscale=False),
    row=2, col=2)

fig.update_layout(
    title_text='Greeks',
    height=1000,
    width=1000
)

import dash
import dash_core_components as dcc
import dash_html_components as html
#app = dash.Dash()
#app.layout = html.Div([
#    dcc.Graph(figure=fig)
#])

import flask

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)

#fig.show()
