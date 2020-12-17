import os
from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
#from backend.sql import add_requester

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello! Grocery Hunters here!</h1>'


def get_messages():
    messages = session.get('message')
    if messages is None:
        session['messages'] = []
        messages = session['messages']# to store messages you may use a dictionary

    return messages

# address = ""
# zip_code = 0
# request_detail = ""
# additional_info = ""
# thank_u_note = ""
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    messages = get_messages()
    print(request)
    body = request.values.get('Body', None)
    # Start our TwiML response
    resp = MessagingResponse()
    if body == 'hi':
        messages = [] # clear up history
        resp.message("Hi! Thanks for using grocery hunters. We are non-profit organization to help connect volunteer to you and help you buy grocery and stuff.\n can I have your name?")
    elif len(messages) == 0:
        messages.append(str(body))
        body = "Hi! "+ str(body) + ", may I have your address? It will only be released to our verified volunteer"
        resp.message(body)
    elif len(messages) == 1:
        messages.append(str(body))
        resp.message("Got ya! And what is your Zip Code number?")
    elif len(messages) == 2:
        messages.append(str(body))
        resp.message("Now you can write your request(items, amount of the items, and specific store with the location, estimate price etc)")
    elif len(messages) == 3:
        messages.append(str(body))
        resp.message("Do you have any drop off details? (Like Front door, can knock on the door, entry requirements) You can answer No if there is no")
    elif len(messages) == 4:
        messages.append(str(body))
        resp.message("Any thank you note for your the volunteer?")
    elif len(messages) == 5:
        messages.append(str(body))
        resp.message("You are all set! you will be notified when a volunteer is matched! Stay safe!")

        add_requester("‭+85292632962‬", messages[0], messages[1], messages[2], messages[3], messages[4], messages[5])
    session['message'] = messages


    return str(resp)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    from waitress import serve
    serve(app, host="127.0.0.1", port=8080)
