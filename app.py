import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import pickle
import numpy as np
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
# app.config.suppress_callback_exceptions = True

df = pd.read_csv('data/indian_liver_patient_cleaned.csv')

# ISI HTML DI SINI

# FORM PREDIKSI
input_groups = dbc.FormGroup(
    [
        dbc.Label('Age'),
        dbc.Input(placeholder='17', type='number', id='age', value=0),
        
        dbc.Label('Gender'),
        dbc.Select(
            options=[
                {'label': 'Male', 'value': 0},
                {'label': 'Female', 'value': 1},
            ], id='gender', value='0'
        ),

        dbc.Label('Total Bilirubin'),
        dbc.Input(placeholder='10.7', type='number', id='tbilirubin', value=0),

        dbc.Label('Direct Bilirubin'),
        dbc.Input(placeholder='1.7', type='number', id='dbilirubin', value=0),

        dbc.Label('Alkaline Phosphotase'),
        dbc.Input(placeholder='177', type='number', id='alka', value=0),

        dbc.Label('Alamine Aminotransferase'),
        dbc.Input(placeholder='109', type='number', id='alam', value=0),

        dbc.Label('Aspartate Aminotransferase'),
        dbc.Input(placeholder='18', type='number', id='aspar', value=0),

        dbc.Label('Total Protiens'),
        dbc.Input(placeholder='7.1', type='number', id='tprotein', value=0),
 
        dbc.Label('Albumin'),
        dbc.Input(placeholder='2.6', type='number', id='albumin', value=0),
 
        dbc.Label('Albumin and Globulin Ratio'),
        dbc.Input(placeholder='0.9', type='number', id='agr', value=0),

        dbc.Button('Predict', color='success', className='mt-3', id='predict'),
    ]
)


# END

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2('Final Project JC-DS 6 Purwadhika Kampus Jakarta'),
                        html.P(
                            '''\
                            Final project ini dikerjakan oleh Nur Wibowo. Pada final project ini
                            menggunakan data Indian Liver Patient Records yang bersumber dari Kaggle
                            (link: https://www.kaggle.com/uciml/indian-liver-patient-records).
                            '''
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            html.H2(
                                                dbc.Button(
                                                    'Menu 1',
                                                    color='link',
                                                    id='group-1-toggle',
                                                )
                                            )
                                        ),
                                        dbc.Collapse(
                                            dbc.CardBody(),
                                            id='collapse-1',
                                        ),

                                        dbc.CardHeader(
                                            html.H2(
                                                dbc.Button(
                                                    'Menu 2',
                                                    color='link',
                                                    id='group-2-toggle',
                                                )
                                            )
                                        ),
                                        dbc.Collapse(
                                            dbc.CardBody('This is the content of group...'),
                                            id='collapse-2',
                                        ),

                                        dbc.CardHeader(
                                            html.H2(
                                                dbc.Button(
                                                    'Prediction',
                                                    color='link',
                                                    id='group-3-toggle',
                                                )
                                            )
                                        ),
                                        dbc.Collapse(
                                            dbc.CardBody(input_groups),
                                            id='collapse-3',
                                        ),
                                    ]
                                )
                            ]
                        ),

                        html.Div(
                            [
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader('Prediction Result'),
                                        dbc.ModalBody([],id='msg'),
                                        dbc.ModalFooter(
                                            dbc.Button('Close', id='close', className='ml-auto')
                                        ),
                                    ],
                                    id='modal',
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('made with <3 in south jakarta by nurwibowo'),
                    ], md=4, className='mt-5 align-items-center',
                ),
            ]
        )

    ], 
    className='mt-5',
)

app.layout = html.Div([body])


# accordion
@app.callback(
    [Output('collapse-1', 'is_open'),
    Output('collapse-2', 'is_open'),
    Output('collapse-3', 'is_open')],
    [Input('group-1-toggle', 'n_clicks'),
    Input('group-2-toggle', 'n_clicks'),
    Input('group-3-toggle', 'n_clicks')],
    [State('collapse-1', 'is_open'),
    State('collapse-2', 'is_open'),
    State('collapse-3', 'is_open')],
)
def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ''
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'group-1-toggle' and n1:
        return not is_open1, False, False
    elif button_id == 'group-2-toggle' and n2:
        return False, not is_open2, False
    elif button_id == 'group-3-toggle' and n3:
        return False, False, not is_open3
    return False, False, False

# predict
@app.callback(
    Output('modal', 'is_open'),
    [Input('predict', 'n_clicks'), Input('close', 'n_clicks')],
    [State('modal', 'is_open')]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('msg','children'),
    [Input('predict','n_clicks')],
    [State('age', 'value'),
    State('gender', 'value'),
    State('tbilirubin', 'value'),
    State('dbilirubin', 'value'),
    State('alka', 'value'),
    State('alam', 'value'),
    State('aspar', 'value'),
    State('tprotein', 'value'),
    State('albumin', 'value'),
    State('agr', 'value')]
)
def predict_liver(n_clicks,age,gender,tbilirubin,dbilirubin,alka,alam,aspar,tprotein,albumin,agr):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    pred_model = pickle.load(open('model_ilp', 'rb'))

    if age == '0' or gender == '' or tbilirubin == '0' or dbilirubin == '0' or alka == '0' or alam == '0' or aspar == '0' or tprotein == '0' or albumin == '0' or agr == '0':
        children = 'Please check the value you input'
    else:
        predict_result = pred_model.predict_proba([[float(age),float(gender),float(tbilirubin),float(dbilirubin),float(alka),float(alam),float(aspar),float(tprotein),float(albumin),float(agr)]])[0][1]
        pds = pred_model.predict([[float(age),float(gender),float(tbilirubin),float(dbilirubin),float(alka),float(alam),float(aspar),float(tprotein),float(albumin),float(agr)]])

        if pds == 1:
            children = 'Sorry, the patient probably has liver disease with probability: {:0.2f}'.format(predict_result)
        else:
            children = 'Well, the patient has not liver disease with probability: {:0.2f}'.format(predict_result)
    
    return children


if __name__ == '__main__':
    app.run_server(debug=True)

