from config import API_SID, ACCOUNT_SID, AUTH_TOKEN, SEND_FROM
from twilio.rest import Client

class TwilioApi:
    def __init__(self):
        self._client = Client(API_SID, AUTH_TOKEN, ACCOUNT_SID)
    
    def send_message(self, phone_numbers, message):
        for phone_number in phone_numbers:
            self._client.messages \
            .create(
                body=message,
                from_=SEND_FROM,
                to=phone_number
            )
