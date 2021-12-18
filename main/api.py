import json
import logging
from main.schemes.tg_message import TGRequest
import aiohttp
import requests
from django.core.handlers.wsgi import WSGIRequest
from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.responses import Response

api = NinjaAPI(urls_namespace='main:api')
logger = logging.getLogger(__package__)
TURL = "https://api.telegram.org/bot%s/%s"


@api.exception_handler(ValidationError)
def send_exceprion_message(request: WSGIRequest, exc):
    message = json.loads(request.body)['message']
    sync_send_message(message['chat']['id'], f"Ошибка! Вы отправили неподдерживаемый файл.")
    return api.create_response(request, {}, status=200)


@api.post('webhook', url_name='webhook')
async def test_hook(request: WSGIRequest, tg_request: TGRequest) -> Response:
    logger.info('Receive message')
    message = tg_request.message
    logger.error(message)
    await send_message(message.chat.id, message.text)
    return Response(data=None, status=200)


@api.get('webhook', url_name='webhook')
def test_hook(request: WSGIRequest) -> Response:
    logger.info('Receive message')
    logger.info(str(request.body))

    return Response(data=None, status=200)


async def send_message(chat_id, text):
    message = {
        'chat_id': chat_id,
        'text': text
    }
    await _request('sendMessage', message)


def sync_send_message(chat_id, text):
    message = {
        'chat_id': chat_id,
        'text': text
    }
    _sync_request('sendMessage', message)


async def _request(method, message):
    headers = {
        'Content-Type': 'application/json'
    }
    resp = requests.post(TURL % ("2090537301:AAGq1hM-yfl7PvfGY5LSS04ysodAB3bAbvU", method),
                         data=json.dumps(message),
                         headers=headers)
    try:
        assert resp.status_code == 200
    except AssertionError:
        pass


def _sync_request(method, message):
    headers = {
        'Content-Type': 'application/json'
    }
    resp = requests.post(TURL % ("2090537301:AAGq1hM-yfl7PvfGY5LSS04ysodAB3bAbvU", method),
                         data=json.dumps(message),
                         headers=headers)
    try:
        assert resp.status_code == 200
    except AssertionError:
        pass
