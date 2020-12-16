# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC93754007201fe05c254e4913ac42d4d2'  #os.environ['TWILIO_ACCOUNT_SID']
auth_token = '4f2462393b39b472cdd714184f4dba23' #os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='McAvoy or Stewart? These timelines can get so confusing.',
         from_='+12516072432',
         status_callback='http://postb.in/1234abcd',
         to='+8618665382225'
     )

print(message.sid)
