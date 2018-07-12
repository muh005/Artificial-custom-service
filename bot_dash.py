import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html 

import requests
import json
import sys
import random
import math

requrl = "http://ip:port/aitele-app/service/chat/v1/tech-asr"
headers = {"Content-type": "application/json; charset=UTF-8"}
data = {}
session = math.floor(1000 * random.random())
conv_hist = []

corpus = {"1":"Hello, I am the customer service trail of Lu Fund, which is specially designed to help customers do asset allocation. Recently, we are about to have a star product on the shelves, I think it is suitable for you. Do you have time to figure out?",
          "2":"This is an equity-based investment project that invests in companies that are not yet listed on the market but are valuable. Have you ever been heard of this type of product before?",
          "3":"Oh, ok. Simply tell you about the fact that the fund we raised this time will be invested in Nanfu Battery, a leading domestic alkaline battery company. I don’t know if you are interested?",
          "4":"Our project is an equity private equity fund. The term is 3+2 years, and the initial investment amount is 1 million. In the future, it will be obtained through the independent listing of Nanfu or being acquired by M&A. Our project is a private equity fund. The term is 3+2 years, and the initial investment amount is 1 million. In the future, it will be obtained through the independent listing of Nanfu or by merger and acquisition.",
          "5":"After the product expires, if the Nanfu battery is not successfully listed, the owners of the repurchased Fang Yafeng Group and Fangding Investment will provide an annual repurchase of 8%. They also have the ability to buy back.",
          "6":"Our project is 3+2 years combo. If Nanfu fails to go public before the end of 2020, it will repurchase at 10% annualized income. If Nanfu is successfully listed before 2020, there will be a two-year capital withdrawal period, and the principal and income will be settled after exit.",
          "7":"Equity projects are not promised, mainly depending on the appreciation of investment projects. The valuation we entered this time is relatively low. As a stable growth industry leader, the future of Nanfu is still worth looking forward to.",
          "8":"Our project has a starting amount of 1 million yuan and a subscription fee of 2%. This threshold is very low compared to other equity projects.",
          "9":"The manager of our contractual fund level is Shanghai Zhichen Management Co., Ltd.",
          "10":"The reason why I introduce this project to you is that there are many investment opportunities, but good projects are rare. This is our star project this year, the recruitment time is short, I hope you have the opportunity to understand",
          "11":"Excuse me, the signal was not very good, can you say it again?",
          "12":"My phone number is 888-888-8888. Welcome to consult. If there is anything, I will provide you with services. Do you have any questions?",
          "13":"Then, will I call you later, when is it convenient?",
          "14":"Ok, we will call you again, thank you for your cooperation, goodbye.",
          "15":"I am sorry to bother you, I wish you a happy life, goodbye.",
          "16":"Ok, then there will be a voice version of the product interpretation sent to your phone, you can understand the product details when you have time. If you have more questions after listening, you can call us. I am sorry to bother you, I wish you a happy life, thank you",
          "17":"Sorry, your question may require a more professional person to answer. I will send the voice version of the product brief to your mobile phone later. You can listen to it when you have time. If you have more questions after listening, you can also consult your account manager or investment consultant. I wish you a happy life, goodbye.",
          "18":"Do you still want to know more about the project?",
          "19":"Hello. I am listening"}


app = dash.Dash()
app.css.append_css({"external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"})

# app ui
app.layout = html.Div([
    html.H3('ASR交互 Demo', style={'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Table([
                html.Tr([
                    # text input for user message
                    html.Td([dcc.Input(id='msg_input', value='', type='text')],
                            style={'valign': 'middle'}),                                              
                    # message to send user message to bot backend
                    html.Td([html.Button('Send', id='send_button', type='submit')],
                            style={'valign': 'middle'})
                ])
            ])],
            style={'width': '325px', 'margin': '0 auto'}),
        html.Br(),
        html.H5(corpus['1'], style={'text-align': 'right','color': '#6495ED'}),
        html.Div(id='conversation')],
        id='screen',
        style={'width': '400px', 'margin': '0 auto'})
])

# trigger bot response to user inputted message on submit button click
@app.callback(
    Output(component_id='conversation', component_property='children'),
    [Input(component_id='send_button', component_property='n_clicks')],
    #[Input(component_id='btn_input', component_property='n_clicks')],
    state=[State(component_id='msg_input', component_property='value')]
    #state=[State(component_id='btn_input', component_property='value')]
)

def update(click, text):
    global conv_hist

    if click is not None:
        if text is not '':
            request = math.floor(100000000000000*random.random())
            data['requestId'] = str(request)
            data['sessionId'] = str(session)
            data['phoneNo'] = '13306620000'
            data['waitTimeout'] = 'false'
            data['asrKnown'] = 'false'  
            data['content'] = text

            JsonStr = json.dumps(data, ensure_ascii=False)
            print(JsonStr)
            #response = requests.post(requrl, data=JsonStr, headers=headers)
            #JsonRes = json.loads(response)
            #resString = JsonRes['data']['voiceId']
        
            req = [html.H5(text, style={'text-align': 'left'})]
            #res = [html.H5(resString, style={'text-align': 'right','color': '#6495ED'})] 

            conv_hist = req + [html.Hr()] + conv_hist

        return conv_hist
    else:
        return ''

@app.callback(
    Output(component_id='msg_input', component_property='value'),
    [Input(component_id='conversation', component_property='children')]
    #state=[State(component_id='btn_input', component_property='value')]
)
def clear_input(_):
    return ''

# run app
if __name__ == '__main__':
    app.run_server()

