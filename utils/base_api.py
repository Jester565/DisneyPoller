import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

URL = None
URL_VAR = None
MAX_TRIES = 5
DEFAULT_ALLOWED_RETRY_METHODS = {'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT', 'TRACE', 'POST'}


class BaseApi:
    def _requests_retry_session(
        self,
        retries=MAX_TRIES,
        backoff_factor=1,
        status_forcelist=[429] + list(range(500, 600)),
        session=None,
        allowed_methods=DEFAULT_ALLOWED_RETRY_METHODS
    ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=allowed_methods,
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _throw_on_invalid_response(self, response):
        response.raise_for_status()
