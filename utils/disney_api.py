
from base_api import BaseApi
from datetime import datetime

LOGIN_TTL = 15552000
TIMEOUT = 30

class DisneyApi(BaseApi):
    def get_api_token(self):
        response = self._requests_retry_session().post(
            'https://authorization.go.com/token',
            data={
                'grant_type': 'assertion',
                'assertion_type': 'public',
                'client_id': 'TPR-DLR-LBJS.WEB-PROD'
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    
    def get_access_token(self, dis_id, refresh_token, api_token):
        epoch_millis = int(datetime.now().timestamp() * 1000)
        response = self._requests_retry_session().post(
            'https://api.wdpro.disney.go.com/profile-service/v4/clients/TPR-DLR-LBJS.WEB-PROD/guests/login/refreshToken',
            json={
                'refreshToken': refresh_token,
                'accessToken': api_token,
                'apiToken': api_token,
                'disID': dis_id,
                'loginTime': epoch_millis,
                'loginTTL': 15552000,
                'refreshTime': epoch_millis
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    
    def get_park_reservation_availability(self, pass_id, sku, access_token):
        response = self._requests_retry_session().get(
            f'https://cme-wdw.wdprapps.disney.com/availability/api/v2/availabilities?sku={sku}&visual-ids={pass_id}',
            headers={
                'Authorization': f'BEARER {access_token}',
                'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': '*/*',
                'User-Agent': 'PostmanRuntime/7.36.1'
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()
