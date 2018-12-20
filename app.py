import os
from flask import Flask, request, Response, make_response, jsonify, url_for, redirect, session, render_template
# Twilio Helper Library
#from twilio.rest import Client
#from twilio.twiml.voice_response import VoiceResponse, Record, Gather, Say, Dial, Play
from signalwire.voice_response import VoiceResponse

app = Flask(__name__)

@app.route('/ivr/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    #response = twiml.Response()
    with response.gather(num_digits=1, action=url_for('menu'), method="POST") as g:
        g.say("Thank you for calling ABC Bank." +
              "Press 1, for Banking services. For Credit Card services, press 2." +
              "To hear these options again, stay on the line.", voice="alice", language="en-US", loop=3)
    return str(response)

# Call functions
@app.route('/ivr/menu', methods=['POST'])
def menu():
    selected_option = request.form['Digits']
    option_actions = {'1': _Savings,
                      '2': _Credit_Card}
    if option_actions.has_key(selected_option):
        response = VoiceResponse()
        option_actions[selected_option](response)
        return str(response)
    
    return _redirect_welcome()
 
# Helper Function for Banking Services
def _Savings(response):
    #response = VoiceResponse()
    response.say("This is a test IVR service for Banking Services. Shortly you can do a whole lot more.",
                 voice="alice", language="en-US")
    response.hangup()
    return str(response)

# Helper Function for Credit Card Services
def _Credit_Card(response):
    #response = VoiceResponse()
    response.say(" This is a test IVR service for Credit Card Services. Shortly you can do a whole lot more.",
                 voice="alice", language="en-US")
    response.hangup()
    return str(response)

#Helper function for redirecting to Welcome Menu
def _redirect_welcome():
    response = VoiceResponse()
    response.say("Returning to the main menu", voice="alice", language="en-US")
    response.redirect(url_for('welcome'))
    return Response(str(response), mimetype='text/xml')

# Helper Function for Agent transfer
def _Speak_Agent(response):
    with response.gather(numDigits=1, action=url_for('agent'), method="POST") as g:
        g.say("To call Vijay, press 2. To call Partha, press 3",
              voice="alice", language="en-GB", loop=3)
    return response
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print "Starting app on port %d" % port
    app.run(debug=False, port=port, host='0.0.0.0')
