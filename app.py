import os
from flask import Flask, request, Response, make_response, jsonify, url_for, redirect, session, render_template
# Twilio Helper Library
#from twilio.rest import Client
#from twilio.twiml.voice_response import VoiceResponse, Record, Gather, Say, Dial, Play
from signalwire.voice_response import VoiceResponse

app = Flask(__name__)

#Add global variable
token = os.environ["token"]


@app.route('/ivr/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    response.pause(length=4)
    response.play(digits=token)
    response.pause(length=4)
    response.hangup()
    return str(response)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print "Starting app on port %d" % port
    app.run(debug=False, port=port, host='0.0.0.0')
