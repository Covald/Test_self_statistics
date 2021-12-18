from datetime import datetime
from typing import Optional, List

from ninja import Schema
from pydantic import BaseModel

from main.schemes.tg_chat import TGChat
from main.schemes.tg_user import TGUser


class TGMessage(BaseModel):
    message_id: int
    user: Optional[TGUser]
    date: datetime
    chat: TGChat
    forward_from: Optional[TGUser]
    forward_date: Optional[datetime]
    reply_to_message: Optional['TGMessage']
    text: str


class TGRequest(Schema):
    update_id: int
    message: TGMessage
