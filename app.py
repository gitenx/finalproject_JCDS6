import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import pickle
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
# app.config.suppress_callback_exceptions = True
# nurwibowo

df = pd.read_csv('data/indian_liver_patient_cleaned.csv')

# ISI HTML DI SINI

# FORM PREDIKSI
input_groups = dbc.FormGroup(
    [
        dbc.Label('Age'),
        dbc.Input(placeholder='17', type='number', min=0, id='age', value=0),
        
        dbc.Label('Gender'),
        dbc.Select(
            options=[
                {'label': 'Male', 'value': 0},
                {'label': 'Female', 'value': 1},
            ], id='gender', value='0'
        ),

        dbc.Label('Total Bilirubin'),
        dbc.Input(placeholder='10.7', type='number', min=0, id='tbilirubin', value=0),

        dbc.Label('Direct Bilirubin'),
        dbc.Input(placeholder='1.7', type='number', min=0, id='dbilirubin', value=0),

        dbc.Label('Alkaline Phosphotase'),
        dbc.Input(placeholder='177', type='number', min=0, id='alka', value=0),

        dbc.Label('Alamine Aminotransferase'),
        dbc.Input(placeholder='109', type='number', min=0, id='alam', value=0),

        dbc.Label('Aspartate Aminotransferase'),
        dbc.Input(placeholder='18', type='number', min=0, id='aspar', value=0),

        dbc.Label('Total Protiens'),
        dbc.Input(placeholder='7.1', type='number', min=0, id='tprotein', value=0),
 
        dbc.Label('Albumin'),
        dbc.Input(placeholder='2.6', type='number', min=0, id='albumin', value=0),
 
        dbc.Label('Albumin and Globulin Ratio'),
        dbc.Input(placeholder='0.9', type='number', min=0, id='agr', value=0),

        dbc.Button('Predict', color='success', className='mt-3', id='predict'),
    ]
)
# END FORM PREDIKSI

# BAR PLOT
df0 = df[df['Dataset']==0]

df0 = df0.drop(columns=['Gender','Age','Dataset'], axis=1)
cols0 = df0.columns
mean0 = df0.mean(axis=0, skipna=True)


df1 = df[df['Dataset']==1]

df1 = df1.drop(columns=['Gender','Age','Dataset'], axis=1)
cols1 = df1.columns
mean1 = df1.mean(axis=0, skipna=True)

people0 = []
people1 = []

for x,y in zip(cols0,mean0):
    people0.append([x,y,'not diseased'])
for x,y in zip(cols1,mean1):
    people1.append([x,y,'diseased'])
    
df_chem0 = pd.DataFrame(people0,columns=['chemicals','mean','status'])
df_chem1 = pd.DataFrame(people1,columns=['chemicals','mean','status'])

bar_plot = dcc.Graph(figure=go.Figure(
                        data=[
                            go.Bar(
                                x=df_chem0['chemicals'],
                                y=df_chem0['mean'],
                                name='Healthy',
                                marker=go.bar.Marker(
                                    color='rgb(55, 83, 109)'
                                )
                            ),
                            go.Bar(
                                x=df_chem1['chemicals'],
                                y=df_chem1['mean'],
                                name='Not Healthy',
                                marker=go.bar.Marker(
                                    color='rgb(26, 118, 255)'
                                )
                            ),
                        ],
                        layout=go.Layout(
                                title='Amount Chemicals in Healthy and Non-Healthy People Body',
                                showlegend=True,
                                legend=go.layout.Legend(
                                    x=0,
                                    y=1.0
                                ),
                                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                            )
                        ),
                        style={'height': 400, 'width': 600},
                        id='my-graph'
                    )
# END BAR PLOT

# HOW TO 
how_to = dbc.ListGroup(
    [
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading('Imunisasi sejak dini'),
                dbc.ListGroupItemText('Hepatitis, sebuah jenis peradangan hati, dapat dicegah dengan pemberian imunisasi sejak dini. Misalnya, imunisasi hepatitis B yang diberikan sejak bayi lahir dan dilakukan dalam beberapa tahap. Begitu pun vaksin hepatitis A yang berfungsi mencegah kita terjangkit penyakit tersebut. Bawa bayi dan anak Anda ke dokter atau sarana kesehatan setempat seperti Posyandu untuk mendapatkan vaksinasi secara teratur.'),
            ]
        ),
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading('Minum air yang banyak'),
                dbc.ListGroupItemText('Air adalah salah satu bagian penting yang berpengaruh di dalam fungsi tubuh kita. Air membantu menghilangkan racun dan melakukan proses penyerapan terhadap nutrisi penting. Meminum air dalam jumlah yang diperlukan juga dapat membantu menghilangkan efek samping selama pengobatan atau terapi. Tetapi perlu juga diperhatikan, apabila Anda sudah mengalami sirosis yaitu hati yang mengalami pengerutan, pengurangan cairan perlu dilakukan agar tubuh Anda mengandung terlalu banyak cairan.'),
            ]
        ),
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading('Makan makanan bergizi'),
                dbc.ListGroupItemText('Pengaturan makanan, baik secara jenis dan jumlah yang tepat, dapat membantu hati untuk mengatur lalu lintas metabolisme dengan baik. Selain itu, kita pun membantu meringankan kerja hati. Fatty liver atau perlemakan hati terjadi karena kita tidak mengatur jumlah lemak dan karbohidrat yang kita makan.'),
            ]
        ),
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading('Hindari alkohol dan Rokok'),
                dbc.ListGroupItemText('Alkohol dapat menyebabkan pengerutan hati atau sirosis. Dalam jangka panjang, alkohol juga dapat menyebabkan kanker hati. Oleh sebab itu, hindari konsumsi alkohol demi kesehatan hati kita. Merokok dapat mengganggu kemampuan hati untuk memetabolisme dan mengeluarkan berbagai jenis zat racun dari dalam tubuh. Selain itu, merokok juga dapat memperburuk kesehatan hati yang telah mengalami gangguan akibat konsumsi minuman beralkohol.'),
            ]
        ),
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading('Hati-hati dalam mengonsumsi obat'),
                dbc.ListGroupItemText('Hati berfungsi untuk mengubah zat obat menjadi aktif atau netral. Banyak obat yang dijual bebas, misalnya obat demam, obat batuk, dan suplemen tubuh dapat menjadi racun bagi hati bila dikonsumsi berlebihan dan tanpa aturan yang jelas. Bila kita tidak berhati-hati dalam memilih obat atau suplemen, hal tersebut akan memperberat kerja hati. Oleh sebab itu, selalu konsultasikan terlebih dahulu dengan dokter Anda, sebelum memulai terapi atau mengonsumsi suplemen tertentu.'),
            ]
        ),
    ]
)

# END HOW TO

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
                            menggunakan data Indian Liver Patient Records yang bersumber dari Kaggle.
                            '''
                        ),
                        html.A('Kaggle: Indian Liver Patient Records', href='https://www.kaggle.com/uciml/indian-liver-patient-records'),
                        html.P('email: nurtriww@gmail.com - github: gitenx')
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
                                                    'Prediction',
                                                    color='link',
                                                    id='group-1-toggle',
                                                )
                                            )
                                        ),
                                        dbc.Collapse(
                                            dbc.CardBody(input_groups),
                                            id='collapse-1',
                                        ),

                                        dbc.CardHeader(
                                            html.H2(
                                                dbc.Button(
                                                    'Amount Chemicals in Healthy and Non-Healthy People Body',
                                                    color='link',
                                                    id='group-2-toggle',
                                                )
                                            )
                                        ),
                                        dbc.Collapse(
                                            dbc.CardBody(bar_plot),
                                            id='collapse-2',
                                        ),

                                        dbc.CardHeader(
                                            html.H2(
                                                dbc.Button(
                                                    'How to Keep Your Liver Healthy / Cara Menjaga Kesehatan Hati',
                                                    color='link',
                                                    id='group-3-toggle',
                                                )
                                            )
                                        ),
                                        dbc.Collapse(
                                            dbc.CardBody([how_to, html.A('Sumber', href='https://hellosehat.com/hidup-sehat/tips-sehat/5-cara-menjaga-kesehatan-hati/')]),
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

    if age == 0 or tbilirubin == 0 or dbilirubin == 0 or alka == 0 or alam == 0 or aspar == 0 or tprotein == 0 or albumin == 0 or agr == 0 or age == '' or tbilirubin == '' or dbilirubin == '' or alka == '' or alam == '' or aspar == '' or tprotein == '' or albumin == '' or agr == '':
        children = dbc.Alert('You can\'t submit null or zero value!', color='danger')
    else:
        # nodisease = pred_model.predict_proba([[float(age),float(gender),float(tbilirubin),float(dbilirubin),float(alka),float(alam),float(aspar),float(tprotein),float(albumin),float(agr)]])[0][0]
        # disease = pred_model.predict_proba([[float(age),float(gender),float(tbilirubin),float(dbilirubin),float(alka),float(alam),float(aspar),float(tprotein),float(albumin),float(agr)]])[0][1]
        pds = pred_model.predict([[float(age),float(gender),float(tbilirubin),float(dbilirubin),float(alka),float(alam),float(aspar),float(tprotein),float(albumin),float(agr)]])

        if pds == 1:
            # children = dbc.Alert('The patient probably has liver disease with probability: {:0.2f}'.format(disease), color='danger')
            children = dbc.Alert('The patient has liver disease', color='danger')
        else:
            # children = dbc.Alert('The patient probably has no liver disease with probability: {:0.2f}'.format(nodisease), color='success')
            children = dbc.Alert('The patient doesn\'t have liver disease', color='success')
    
    return children



if __name__ == '__main__':
    app.title = 'Final Project: Liver Detection'
    app.run_server(debug=False)

