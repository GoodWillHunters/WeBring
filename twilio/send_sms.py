# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

def send_msg_to_requester(phone_number, requester_name, volunteer_name):
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = ''  #os.environ['TWILIO_ACCOUNT_SID']
    auth_token = '' #os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
             body='Hi ' + requester_name + ', ' + volunteer_name + ' has taken your request! They will approach soon!',
             from_='+18135484923',
             to=phone_number
         )


print(message.sid)
