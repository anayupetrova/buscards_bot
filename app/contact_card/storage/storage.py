import uuid
from abc import ABC

from app.contact_card.contact_card import ContactCard


class ContactStorage(ABC):
    """
    Абстрактный класс хранилища контактов
    """
    def get(self, uuid: uuid.UUID) -> ContactCard:
        """
        Получение контакта из хранилища
        """
        pass

    def put(self, contact: ContactCard) -> uuid.UUID:
        """
        Добавление контакта в хранилище
        """
        pass
