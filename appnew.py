import os
from flask import Flask, request, Response, make_response, jsonify, url_for, redirect, session, render_template
# Twilio Helper Library
#from twilio.rest import Client
#from twilio.twiml.voice_response import VoiceResponse, Record, Gather, Say, Dial, Play
from signalwire.voice_response import VoiceResponse, Record, Gather, Say, Dial, Play

app = Flask(__name__)

# Main Menu
@app.route('/ivr/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    with response.gather(num_digits=1, timeout=25, action=url_for('menu'), method="POST") as g:
        g.pause(length=4)
        g.say("Thank you for calling ABC Bank" +
              "Press 1, for Banking services. For Credit Card services, press 2.", voice="alice", language="en-US")
    return str(response)

# Sub Menu 1
@app.route('/ivr/menu', methods=['POST'])
def menu():
    selected_option = request.form['Digits']
    print("Selected option is => " + selected_option)
    if selected_option == '1':
        response = VoiceResponse()
        with response.gather(num_digits=1, timeout=25, action=url_for('menubank'), method="POST") as g:
            g.say("Press 1 for Account Balance. For any other information press 2.", voice="alice", language="en-US")
        return str(response)
    if selected_option == '2':
        response = VoiceResponse()
        with response.gather(num_digits=1, timeout=25, action=url_for('menucredit'), method="POST") as g:
            g.say("Press 1 for Due amount. For any other information press 2.", voice="alice", language="en-US")
        return str(response)
    return _redirect_welcome()

#Sub Menu 2-banking
@app.route('/ivr/menu/menubank', methods=['POST'])
def menubank():
    selected_option = request.form['Digits']
    print("Selected option is => " + selected_option)
    if selected_option =='1':
        response = VoiceResponse()
        with response.gather(num_digits=7, timeout=25, action=url_for('accbalance'), method="POST") as g:
            g.say("Please provide your account number", voice="alice", language="en-US")
        return str(response)
     if selected_option == '2':
        response = VoiceResponse()
        response.say("We are in the process of setting up other banking services. Shortly you can do a whole lot more", voice="alice", language="en-US")
        #with response.gather(num_digits=1, timeout=25, action=url_for('menucredit'), method="POST") as g:
            #g.say("We are in the process of setting up other banking services. Shortly you can do a whole lot more", voice="alice", language="en-US")
        response.hangup()
        return str(response)
    
#Sub Menu 2-credit card
@app.route('/ivr/menu/menucredit', methods=['POST'])
def menucredit():
    selected_option = request.form['Digits']
    print("Selected option is => " + selected_option)
    if selected_option =='1':
        response = VoiceResponse()
        with response.gather(num_digits=7, timeout=25, action=url_for('dueamount'), method="POST") as g:
            g.say("Please provide your account number", voice="alice", language="en-US")
        return str(response)
     if selected_option == '2':
        response = VoiceResponse()
        response.say("We are in the process of setting up other credit card services. Shortly you can do a whole lot more", voice="alice", language="en-US")
        #with response.gather(num_digits=1, timeout=25, action=url_for('menucredit'), method="POST") as g:
            #g.say("We are in the process of setting up other credit card services. Shortly you can do a whole lot more", voice="alice", language="en-US")
        response.hangup()
        return str(response)
     
# Sub Menu 3-banking
@app.route('/ivr/menu/accbalance', methods=['POST'])
def menubank():
    account_number = request.form['Digits']
    response = VoiceResponse()
    if account_number == '1234567':
        response.say("Your savings account balance is ten thousand dollars", voice="alice", language="en-US")
        response.hangup()
        return str(response)
    elif account_number == '7654321':
        response.say("Your savings account balance is ten thousand dollars", voice="alice", language="en-US")
        response.hangup()
        return str(response)
    else:
        response.say("I am sorry, you have provided an incorrect account number. Goodbye", voice="alice", language="en-US")
        response.hangup()
        return str(response)
        
    '''
    option_actions = {'1': _AccountBalance,
                      '2': _OtherBank}
    if option_actions.has_key(selected_option):
        response = VoiceResponse()
        option_actions[selected_option](response)
        return str(response)
    return _redirect_menu()
    '''
    
# Sub Menu 3-credit card
@app.route('/ivr/menu/dueamount', methods=['POST'])
def menubank():
    account_number = request.form['Digits']
    response = VoiceResponse()
    if account_number == '1234567':
        response.say("Your total due amount is five hundred dollars", voice="alice", language="en-US")
        response.hangup()
        return str(response)
    elif account_number == '7654321':
        response.say("Your total due amount is eight hundred dollars", voice="alice", language="en-US")
        response.hangup()
        return str(response)
    else:
        response.say("I am sorry, you have provided an incorrect account number. Goodbye", voice="alice", language="en-US")
        response.hangup()
        return str(response)
'''
# Sub Menu 2-credit card
@app.route('/ivr/menu/menucredit', methods=['POST'])
def menucredit():
    selected_option = request.form['Digits']
    option_actions = {'1': _DueAmount,
                      '2': _OtherCredit}
    if option_actions.has_key(selected_option):
        response = VoiceResponse()
        option_actions[selected_option](response)
        return str(response)
    return _redirect_menu()

# Helper Function for Banking Services-Account Balance
def _AccountBalance(response):
    #response = VoiceResponse()
    response.say("We are currently testing our services. You can hear your account balance once we have launched the service.",
                 voice="alice", language="en-US")
    response.hangup()
    return str(response)

# Helper Function for Banking Services-Others
def _OtherBank(response):
    #response = VoiceResponse()
    response.say("We are in the process of setting up our banking services. Shortly you can do a whole lot more.",
                 voice="alice", language="en-US")
    response.hangup()
    return str(response)

# Helper Function for Banking Services-Account Balance
def _DueAmount(response):
    #response = VoiceResponse()
    response.say("We are currently testing our services. You can hear your payment due amount once we have launched the service.",
                 voice="alice", language="en-US")
    response.hangup()
    return str(response)

# Helper Function for Credit card Services-Others
def _OtherCredit(response):
    #response = VoiceResponse()
    response.say("We are in the process of setting up our credit card services. Shortly you can do a whole lot more.",
                 voice="alice", language="en-US")
    response.hangup()
    return str(response)

#Helper function for redirecting to Main Menu
def _redirect_welcome():
    response = VoiceResponse()
    response.say("Returning to the main menu", voice="alice", language="en-US")
    response.redirect(url_for('welcome'))
    return Response(str(response), mimetype='text/xml')

#Helper function for redirecting to Sub Menu 1
def _redirect_menu():
    response = VoiceResponse()
    response.say("Returning to the previous menu", voice="alice", language="en-US")
    response.redirect(url_for('menu'))
    return Response(str(response), mimetype='text/xml')
'''
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print "Starting app on port %d" % port
    app.run(debug=False, port=port, host='0.0.0.0')
