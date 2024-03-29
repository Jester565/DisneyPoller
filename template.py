from config import ERROR_NOTIFY_NUMBER, NOTIFY_NUMBERS
from utils.disney_api import DisneyApi
from utils.disney_auth_generator import DisneyAuthGenerator
from utils.twilio_api import TwilioApi

POLL_INTERVAL = 45 * 60  # poll every 45 minutes

def run():
    auth_generator = DisneyAuthGenerator()
    disney_api = DisneyApi()
    twilio_api = TwilioApi()
    try:
        # will continue to provide valid access_tokens at 45 minute intervals forever
        for access_token in auth_generator.maintain_valid_auth_tokens(sleep_for=POLL_INTERVAL):
            # TODO: replace with your Disney API calls
            park_availability = disney_api.get_park_reservation_availability(
                'PASS_ID',
                'SKU',
                access_token
            )
            if len(park_availability) > 0:
                twilio_api.send_message(NOTIFY_NUMBERS, 'PARKS ARE AVAILABLE!')
    except Exception as e:
        twilio_api.send_message(
            [ERROR_NOTIFY_NUMBER],
            f'An error occured in park availability script: {e}'
        )
        raise e

if __name__ == "__main__":
    run()
