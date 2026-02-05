import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_SID = os.getenv("MY_TWILLLO_SID")
TWILIO_AUTH_TOKEN = os.getenv("MY_TWILLO_AUTH")
TWILIO_VIRTUAL_NUMBER = os.getenv("MY_TWILLO_VIRTUAL_NUMBER")
TWILIO_VERIFIED_NUMBER = os.getenv("MY_TWILLO_VERIFIED_NUMBER")

# Using a .env file to retrieve the phone numbers and tokens.

class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message_body):
        message = self.client.messages.create(
            from_=TWILIO_VIRTUAL_NUMBER,
            body=message_body,
            to=TWILIO_VERIFIED_NUMBER
        )
        #checks if message was sent succesfully
        print(message.sid)

    # we used sms in previous lessons, you can try whatsapp:
    def send_whatsapp(self, message_body):
        message = self.client.messages.create(
            from_=f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}',
            body=message_body,
            to=f'whatsapp:{os.environ["TWILIO_VERIFIED_NUMBER"]}'
        )
        print(message.sid)