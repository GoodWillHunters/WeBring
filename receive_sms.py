import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello!</h1>'

num = 0
name = ""
address = ""
zip_code = 0
request = ""
additional_info = ""
thank_u_note = ""
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    num += 1
    body = request.values.get('Body', None)
    # Start our TwiML response
    resp = MessagingResponse()
    # Add a message
    if body == 'help': 
        num = 1
        resp.message("Hi! Thanks for using grocery hunters. We are non-profit organization to help connect volunteer to you and help you buy grocery and stuff.\n can I have your name?")
    elif num == 1:
        name = body
        body = ("Hi! ", name, ", may I have your address? It will only be released to our verified volunteer")
        resp.message(body)
    elif num == 2:
        address = body
        resp.message("Got ya! And what is your Zip Code number?")
    elif num == 3:
        zip_code = body
        resp.message("Now you can write your request(items, amount of the items, and specific store with there location, estimate price etc)")
    elif num == 4:
        request = body
        resp.message("Do you have any drop off details? (Like Front door, can knock on the door, entry requirements) You can answer No if there is no")
    elif num == 5:
        additional_info = body
        resp.message("Any thank you note for your the volunteer?")
    elif num == 6:
        thank_u_note = body
        resp.message("You are all set! you will be notified when the driver ")

    return str(resp)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1", port=8080)
