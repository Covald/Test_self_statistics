import json
import logging

from django.core.handlers.wsgi import WSGIRequest
from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.responses import Response

from main.models import Ticket
from main.services import send_message, reply_to_message, download_photo, QRService

api = NinjaAPI(title='Telegram API', urls_namespace='main:api', version='1.0.0',
               description='Описание эндпоинтов для API для телеграмма')
logger = logging.getLogger(__package__)

TOKEN = "2090537301:AAGq1hM-yfl7PvfGY5LSS04ysodAB3bAbvU"


@api.exception_handler(ValidationError)
def send_exception_message(request: WSGIRequest, exc):
    message = json.loads(request.body)['message']
    logger.critical(message)
    send_message(message['chat']['id'], f"Ошибка! Вы отправили неподдерживаемый файл.")
    return api.create_response(request, {}, status=200)


@api.post('webhook', url_name='webhook', tags=['Telegram'], summary='WebHook для telegram.',
          description="Отвечает всегда статусом 200. Если Происходит ошибка, то высылает ее в чат пользователю.")
def test_hook(request: WSGIRequest) -> Response:
    message = json.loads(request.body)["message"]
    logger.debug('Receive message')
    logger.debug(message)
    file_name = None
    if message.get("photo") is not None:
        logger.debug('Receive photo')
        try:
            file_name = download_photo(message)
            reply_to_message(message, 'Фото загружены.')
        except Exception:
            reply_to_message(message, 'Что-то пошло не так с загрузкой фото. :(')

        try:
            qr = QRService()
            qr.process_photo(file_name)
            reply_to_message(message, 'QR обработан и чек сохранен в базе.')
        except Exception as err:
            print(err)
            reply_to_message(message, 'Что-то пошло не так с обработкой QR кода. :(')
    else:
        reply_to_message(message, f'ECHO: {message.get("text")}')
    logger.error('------------------')
    return Response(data=None, status=200)
