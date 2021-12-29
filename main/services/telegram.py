import json
import logging
from datetime import datetime
from typing import Any

import requests
from django.conf import settings

telegram_api_url = "https://api.telegram.org"
logger = logging.getLogger(__package__)


def download_photo(message: dict) -> str:
    photo = message['photo'][-1]
    print(f'processing photo {photo["file_id"]}')
    return _download_file(photo["file_id"])


def reply_to_message(message, text: str) -> None:
    send_message(chat_id=message["chat"]["id"], text=text, reply_to=message["message_id"])


def send_message(chat_id, text, reply_to=None):
    message = {
        'chat_id': chat_id,
        'text': text
    }
    if reply_to:
        message.update({'reply_to_message_id': reply_to})
    _request('/sendMessage', message)


def _download_file(file_id: str):
    headers = {
        'Content-Type': 'application/json'
    }
    url = telegram_api_url + f"/file/bot{settings.TELEGRAM_TOKEN}"
    with requests.Session() as session:
        session.headers.update(headers)
        raw_file = session.post(telegram_api_url + f"/bot{settings.TELEGRAM_TOKEN}/getFile", data=json.dumps({'file_id': file_id}))
        file_path = raw_file.json()['result'].get('file_path')
        if file_path is None:
            raise ValueError('Файл не найден!')
        response_file = session.get(url + f'/{file_path}')
        with open(rf'media/{datetime.now()}.jpg', 'wb') as fp:
            fp.write(response_file.content)
            logger.info(rf"Save file - {fp.name}")
            return fp.name


def _request(method, message) -> Any:
    headers = {
        'Content-Type': 'application/json'
    }
    resp = requests.post(telegram_api_url + "/bot%s%s" % ("2090537301:AAGq1hM-yfl7PvfGY5LSS04ysodAB3bAbvU", method),
                         data=json.dumps(message),
                         headers=headers)
    try:
        assert resp.status_code == 200
        return resp
    except AssertionError:
        pass
