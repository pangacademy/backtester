# notes
'''
This file is for housing the main dash application.
This is where we define the various css items to fetch as well as the layout of our application.
'''
import dash
from dash import  html
import dash_mantine_components as dmc
from flask import Flask
import os

# local imports
from utils.settings import APP_HOST, APP_PORT, APP_DEBUG, DEV_TOOLS_PROPS_CHECK


server = Flask(__name__)
app = dash.Dash( __name__,
    server=server,
    use_pages=True,    # turn on Dash pages
    meta_tags=[
        {   # check if device is a mobile device. This is a must if you do any mobile styling
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1'
        }
    ],
    suppress_callback_exceptions=True,
    title='Machine Learning Finance Challenge Graph',
    external_stylesheets=dmc.styles.ALL)

def serve_layout():
    '''Define the layout of the application'''
    return html.Div(
        [
            html.Div(
                dash.page_container,
                class_name='my-2'
            ),
        ]
    )

if __name__ == '__main__':
    app.run_server(
        host=APP_HOST,
        port=APP_PORT,
        debug=APP_DEBUG,
        dev_tools_props_check=DEV_TOOLS_PROPS_CHECK
    )