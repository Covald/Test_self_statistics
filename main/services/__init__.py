__all__ = ['send_message','reply_to_message', 'download_photo', 'QRService']
from main.services.qrcodes import QRService
from main.services.telegram import send_message, reply_to_message, download_photo
