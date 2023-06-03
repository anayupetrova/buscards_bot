from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, HttpUrl, Field


class ContactCard(BaseModel):
    """
    Класс-dto карточки с контактом.
    Содержит в себе:
        - ФИ
        - Почту
        - Компанию
        - Должность
        - О себе
        - Ссылки на соц. сети
    """
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: Optional[EmailStr]
    company: str
    position: str
    about: str
    avatar_id: str
    social_links: List[HttpUrl]
