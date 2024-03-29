from datetime import datetime, timedelta
from config import INIT_REFRESH_TOKEN, DIS_ID
from disney_api import DisneyApi
from time import sleep

DEFAULT_TTL_BUFFER = 100 # 100 seconds

class DisneyAuthGenerator:
    def __init__(self):
        self._refresh_token = INIT_REFRESH_TOKEN
        self._access_token = None
        self._access_token_expiration_date = None
        self._api_token = None
        self._api_token_expiration_date = None
        self._disney_api = DisneyApi()

    def get_valid_api_token(self):
        if self._api_token_expiration_date is None or self._is_expired(self._api_token_expiration_date):
            api_token_resp = self._disney_api.get_api_token()
            self._api_token = api_token_resp["access_token"]
            self._api_token_expiration_date = self._get_expiration_date_from_ttl(
                int(api_token_resp["expires_in"])
            )
        return self._api_token
    
    def get_valid_access_token(self, ttl_buffer=DEFAULT_TTL_BUFFER):
        if self._access_token_expiration_date is None or self._is_expired(self._access_token_expiration_date, ttl_buffer):
            api_token = self.get_valid_api_token()
            access_token_resp = self._disney_api.get_access_token(
                DIS_ID,
                self._refresh_token,
                api_token,
            )
            self._access_token = access_token_resp["data"]["token"]["access_token"]
            self._refresh_token = access_token_resp["data"]["token"]["refresh_token"]
            ttl = access_token_resp["data"]["token"]["ttl"]
            self._access_token_expiration_date = self._get_expiration_date_from_ttl(ttl)
        return self._access_token

    # yield a valid access_token at sleep_for intervals but also run every ~30 minutes to keep our access_token alive
    def maintain_valid_auth_tokens(self, sleep_for=0, ttl_buffer=DEFAULT_TTL_BUFFER):
        next_run_date = datetime.now()
        while True:
            access_token = self.get_valid_access_token(ttl_buffer)
            if datetime.now() >= next_run_date:
                next_run_date = datetime.now() + timedelta(seconds=sleep_for)
                yield access_token
            seconds_til_expiration = self._seconds_til(self._access_token_expiration_date) - ttl_buffer
            seconds_til_next_run = self._seconds_til(next_run_date)
            seconds_to_sleep = min(seconds_til_expiration, seconds_til_next_run) + 1  # add a second just in case
            sleep(seconds_to_sleep)

    def _get_expiration_date_from_ttl(self, ttl):
        return datetime.now() + timedelta(seconds=ttl)

    def _is_expired(self, expiration_date, ttl_buffer=DEFAULT_TTL_BUFFER):
        return datetime.now() >= expiration_date - timedelta(seconds=ttl_buffer)

    def _seconds_til(self, target_date):
        return max((target_date - datetime.now()).total_seconds(), 0)
