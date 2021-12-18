from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TGChat(BaseModel):
    id: int
    type: str  # TODO: написать класс для Enum
    title: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    all_members_are_administrators: Optional[bool]
