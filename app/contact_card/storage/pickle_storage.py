import pickle
import uuid
from pathlib import Path

from app.contact_card.contact_card import ContactCard
from app.contact_card.storage.storage import ContactStorage


class PickleContactStorage(ContactStorage):
    """
    Хранилище контактов в памяти
    """
    def __init__(self):
        self._contacts = {}
        Path('db').mkdir(exist_ok=True)
        self._pickle_file = Path('db') / 'contacts.pickle'
        self.load_from_pickle()

    def load_from_pickle(self):
        if not self._pickle_file.exists():
            self.save_to_pickle()
            return

        with self._pickle_file.open('rb') as f:
            self._contacts = pickle.load(f)

    def save_to_pickle(self):
        with self._pickle_file.open('wb') as f:
            pickle.dump(self._contacts, f)

    def get(self, c_uuid: uuid.UUID) -> ContactCard:
        return self._contacts.get(c_uuid)

    def put(self, contact: ContactCard) -> uuid.UUID:
        self._contacts[contact.id] = contact
        self.save_to_pickle()
        return contact.id
