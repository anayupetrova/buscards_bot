from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, HttpUrl, Field


class CardComment(BaseModel):
    """
    Класс-dto комментария пользователя к контакту.
    Содержит в себе:
        - uuid контакта
        - id пользователя
        - текст комментария
    """
    card_id: UUID = Field(default_factory=uuid4)
    user_id: int
    text: str
