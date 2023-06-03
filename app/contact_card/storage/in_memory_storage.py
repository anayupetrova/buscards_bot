import uuid

from app.contact_card.contact_card import ContactCard
from app.contact_card.storage.storage import ContactStorage


class InMemoryContactStorage(ContactStorage):
    """
    Хранилище контактов в памяти
    """
    def __init__(self):
        self._contacts = {}

    def get(self, c_uuid: uuid.UUID) -> ContactCard:
        return self._contacts.get(c_uuid)

    def put(self, contact: ContactCard) -> uuid.UUID:
        self._contacts[contact.id] = contact
        return contact.id
