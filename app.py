import os

from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from twilio import twiml
from twilio.rest import TwilioRestClient
from view_helpers import twiml

app = Flask(__name__)

#@app.route('/')
#@app.route('/ivr')
#def home():
    #return render_template('index.html')

@app.route('/ivr/welcome', methods=['POST'])
def welcome():
    response = twilio.twiml.Response()
    with response.gather(numDigits=1, action=url_for('menu'), method="POST") as g:
        g.say("Thank you for calling ABC Bank " +
              "For Banking, press 1. For Credit Card, press 2. To " +
              "hear these options again, stay on the line", voice="alice", language="en-GB", loop=3)
    return twiml(response)


@app.route('/ivr/menu', methods=['POST'])
def menu():
    selected_option = request.form['Digits']
    option_actions = {'1': _Savings,
                      '2': _Credit_Card}

    if option_actions.has_key(selected_option):
        response = twilio.twiml.Response()
        option_actions[selected_option](response)
        return twiml(response)

    return _redirect_welcome()


# private methods

def _Savings(response):
    response.say(" This is a test IVR service for Savings Banking. Once live you can do a whole lot more",
                 voice="alice", language="en-GB")

    response.say("Thank you for calling ABC Bank - the " +
                 "bank for the future")

    response.hangup()
    return response


def _Credit_Card(response):
    response.say(" This is a test IVR service for Credit Card. Once live you can do a whole lot more",
                 voice="alice", language="en-GB")

    response.say("Thank you for calling ABC Bank - the " +
                 "bank for the future")

    response.hangup()
    return response    	


def _redirect_welcome():
    response = twilio.twiml.Response()
    response.say("Returning to the main menu", voice="alice", language="en-GB")
    response.redirect(url_for('welcome'))
    return twiml(response)
    
if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=False)
