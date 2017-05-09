import os
from flask import Flask
from flask import redirect
from flask import url_for
from flask import session
from flask import Response
from flask import request
from flask import render_template
from twilio import twiml
from twilio.rest import TwilioRestClient
import os.path
import sys
import json
#import apiai

try:
	import apiai
except ImportError:
	sys.path.append(
		os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
	)
	import apiai

app = Flask(__name__)

@app.route('/ivr/welcome', methods=['POST'])
def welcome():
	response = twiml.Response()
	with response.gather(numDigits=1, action=url_for('menu'), method="POST") as g:
		g.say("Thank you for calling ABC Bank " + "Press 1, for Account Balance. For Credit Card services, press 2. To speak to an agent, press 3 " +
              "To hear these options again, stay on the line", voice="alice", language="en-GB", loop=3)
	return Response(str(response), mimetype='text/xml')

@app.route('/ivr/menu', methods=['POST'])
def menu():
	selected_option = request.form['Digits']
	option_actions = {'1': _Account_Balance,
                      '2': _Credit_Card,
                      '3': _Speak_Agent}
	
	if option_actions.has_key(selected_option):
		response = twiml.Response()
		option_actions[selected_option](response)
		return Response(str(response), mimetype='text/xml')
	return _redirect_welcome()
    
@app.route('/ivr/agent', methods=['POST'])
def agent():
	selected_option = request.form['Digits']
	option_actions = {'2': "+917338856833",
                      '3': "+919940623555"}
	if option_actions.has_key(selected_option):
		response = twiml.Response()
		response.dial(option_actions[selected_option])
		return Response(str(response), mimetype='text/xml')
	return _redirect_welcome()

# private methods

def _Account_Balance(response):
	CLIENT_ACCESS_TOKEN = '5f910e9e98e54ccb924f606705984a43'
	print (CLIENT_ACCESS_TOKEN)
	ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
	print (ai)
	request = ai.text_request()
	request.lang = 'en'
	#req.session_id = "1232323456"
	request.query = "I want my account balance"
	answer = request.getresponse()
	print (answer)
	answerstr = answer.read().decode('utf-8')
	answer_obj = json.loads(answerstr)
	prompt = answer_obj["result"]["fulfillment"]["speech"]
	response.say("prompt", voice="alice", language="en-GB")
	response.say("Thank you for calling ABC Bank -  " +
                 " The bank of the future")
	response.hangup()
	return response


def _Credit_Card(response):
	response.say(" This is a test IVR service for Credit Card. Shortly you can do a whole lot more",
		     voice="alice", language="en-GB")
	response.say("Thank you for calling ABC Bank - the " +
                 "bank for the future")
	response.hangup()
	return response    	
    
def _Speak_Agent(response):
	with response.gather(numDigits=1, action=url_for('agent'), method="POST") as g:
		g.say("To call Vijay, press 2. To call Partha, press 3",
		      voice="alice", language="en-GB", loop=3)
		return response

def _redirect_welcome():
	response = twiml.Response()
	response.say("Returning to the main menu", voice="alice", language="en-GB")
	response.redirect(url_for('welcome'))
	#return twiml(response)
	return Response(str(response), mimetype='text/xml')
    
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print "Starting app on port %d" % port
	app.run(debug=False, port=port, host='0.0.0.0')
