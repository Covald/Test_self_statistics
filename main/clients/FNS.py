import json
import os

import requests
from django.conf import settings
from dotenv import load_dotenv


class FNSClient:
    HOST = 'irkkt-mobile.nalog.ru:8888'
    DEVICE_OS = 'iOS'
    CLIENT_VERSION = os.getenv('FNS_CLIENT_VERSION')
    DEVICE_ID = '7C82010F-16CC-446B-8F66-FC4080C66521'
    ACCEPT = '*/*'
    USER_AGENT = 'billchecker/2.9.0 (iPhone; iOS 13.6; Scale/2.00)'
    ACCEPT_LANGUAGE = 'ru-RU;q=1, en-US;q=0.9'

    def __init__(self):
        load_dotenv()
        self._session = requests.Session()
        session_id = self._get_session_id()
        self._session.headers = {
            'Host': self.HOST,
            'Accept': self.ACCEPT,
            'Device-OS': self.DEVICE_OS,
            'Device-Id': self.DEVICE_ID,
            'clientVersion': self.CLIENT_VERSION,
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'sessionId': session_id,
            'User-Agent': self.USER_AGENT,
        }

    @property
    def session(self):
        return self._session

    def _get_session_id(self) -> str:
        url = f'https://{self.HOST}/v2/mobile/users/lkfl/auth'
        payload = {
            'inn': settings.FNS_INN,
            'client_secret': settings.FNS_CLIENT_SECRET,
            'password': settings.FNS_PASSWORD
        }
        headers = {
            'Host': self.HOST,
            'Accept': self.ACCEPT,
            'Device-OS': self.DEVICE_OS,
            'Device-Id': self.DEVICE_ID,
            'clientVersion': self.CLIENT_VERSION,
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'User-Agent': self.USER_AGENT,
        }

        resp = requests.post(url, json=payload, headers=headers)
        return json.loads(resp.content)['sessionId']

    def _get_ticket_id(self, parsed_qr: str) -> str:
        url = f'https://{self.HOST}/v2/ticket'
        data = {'qr': parsed_qr}
        resp = self._session.post(url, json=data)
        return resp.json().get("id")

    def get_ticket(self, qr: str) -> dict:
        ticket_id = self._get_ticket_id(qr)
        url = f'https://{self.HOST}/v2/tickets/{ticket_id}'
        resp = self._session.get(url)
        return resp.json()
