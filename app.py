# -*- coding: utf-8 -*-
"""
Created on Thu Apr  23 17:43:39 2020

@author: yasmen amr
"""
import os
import pathlib
import statistics
from collections import OrderedDict

import pathlib as pl
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State

import utils
APP_PATH=os.path.dirname(os.path.abspath(__file__))


book_info = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "items_info222.dat")),sep='\t')
book_ratings = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "book_ratings.dat")),sep='\t',index_col=False)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True




def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))],id='table')])



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
APP_PATH=os.path.dirname(os.path.abspath(__file__))
app.layout = html.Div(children=[
        html.Div(children=[

            html.H2("Book Recommendation",style={'color':'white','textAlign': 'center', 'margin-bottom': 5 ,'background':'#00CCFF','text-height':'500px'}),
            html.A(
                id="gh-link",
                children=["View on GitHub"],
                href="https://github.com/yasmenamr/Book-Recommendations",
                style={"color": "black", "border": "solid 1px white",'background':'#CCFFF'},


                  )
                           ]
                ),
        html.Div(children=[

            html.H4(''),

            dcc.Input(id='input-1-state', type='number', placeholder='enter your id'),
            html.Button(id='submit-button-state', n_clicks =0, children='Submit'),
            html.H4(children='The site will recommend books for you based on what you like'),

            dash_table.DataTable(id='table1',
                                columns=[{"name": i, "id": i} for i in utils.top_5_recommendations(-1).columns] ,
                                style_data={"text-align":"left"},style_header={"text-align":"left"}


                                )

                            ]
                )
                                ]
                    )


@app.callback(Output('table1','data'),
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value')])


def update_output(x,n_clicks):
    return   utils.top_5_recommendations(x).to_dict('records')[:5]


if __name__ == '__main__':
    app.run_server(debug=True)




