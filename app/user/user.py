from typing import List

from pydantic import BaseModel

from app.contact_card import ContactCard


class User(BaseModel):
    """
    Класс-dto пользователя
    Содержит в себе:
        - id пользователя
        - Список его контактных карточек ContactCard
    """
    id: int
    contact_cards: List[ContactCard]
