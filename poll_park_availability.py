from config import ERROR_NOTIFY_NUMBER, NOTIFY_NUMBERS
from utils.disney_api import DisneyApi
from utils.disney_auth_generator import DisneyAuthGenerator
from utils.twilio_api import TwilioApi
from datetime import datetime

# TODO: update with your pass
PASS_ID = ''  # disney pass ID, you can find this on the back of your pass
SKU = 'NBE26' # some kinda constant for employee pass lookup?
POLL_INTERVAL = 45 * 60  # poll every hour

WDW_AK = 'WDW_AK'
WDW_EP = 'WDW_EP'
WDW_HS = 'WDW_HS'
WDW_MK = 'WDW_MK'

ALL_PARKS = [
    WDW_AK,
    WDW_EP,
    WDW_HS,
    WDW_MK
]

PARK_CODES_TO_NAMES = {
    WDW_AK: 'Animal Kingdom',
    WDW_EP: 'Epcot',
    WDW_HS: 'Hollywood Studios',
    WDW_MK: 'Magic Kingdom'
}

WATCH_DATES = {
    '2024-04-20': ALL_PARKS,
    '2024-04-21': ALL_PARKS,
    '2024-04-22': [WDW_EP],
}

def get_available_watched_dates(park_availability):
    available_watched_dates = []
    for date_availability in park_availability['calendar-availabilities']:
        date = date_availability['date']
        watched_parks = WATCH_DATES.get(date)
        if watched_parks is not None:
            facilities = date_availability['facilities']
            available_watched_parks = []
            for facility in facilities:
                facility_code = facility['facilityName']
                if facility['available'] and facility_code in watched_parks:
                    available_watched_parks.append(facility_code)
            if len(available_watched_parks) > 0:
                available_watched_dates.append({
                    'date': date,
                    'parks': available_watched_parks
                })
    return available_watched_dates

def get_availability_message(available_dates):
    msg = 'PARK AVAILABILITY ON:'
    for date_availability in available_dates:
        date = date_availability['date']
        parks = date_availability['parks']
        msg += f'\n{date}:\n'
        for park_code in parks:
            park_name = PARK_CODES_TO_NAMES[park_code]
            msg += f'  -{park_name}\n'
    return msg

def run():
    auth_generator = DisneyAuthGenerator()
    disney_api = DisneyApi()
    twilio_api = TwilioApi()
    try:
        # will continue to provide valid access_tokens at sleep_for intervals forever
        for access_token in auth_generator.maintain_valid_auth_tokens(sleep_for=POLL_INTERVAL):
            print('checking availability at: ', datetime.now())
            park_availability = disney_api.get_park_reservation_availability(
                PASS_ID,
                SKU,
                access_token
            )
            available_dates = get_available_watched_dates(park_availability)
            if len(available_dates) > 0:
                msg = get_availability_message(available_dates)
                print('Sending message: ', msg)
                twilio_api.send_message(NOTIFY_NUMBERS, msg)
    except Exception as e:
        twilio_api.send_message(
            [ERROR_NOTIFY_NUMBER],
            f'An error occured in park availability script: {e}'
        )
        raise e

if __name__ == "__main__":
    run()
