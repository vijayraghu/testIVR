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

app = Flask(__name__)

@app.route('/ivr/welcome', methods=['POST'])
def welcome():
    response = twiml.Response()
     twiml.say("Hello Krishna Raman " +
              "This is a call from Infosys BGC team to inform you that you have defaulted to submit your work experience records	" +
              "Please do the needful at the earliest failing which necessary action would be taken. Thank you", voice="alice", language="en-GB", loop=3)
    return Response(str(response), mimetype='text/xml')
	
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
