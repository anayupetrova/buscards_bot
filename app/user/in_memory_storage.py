from app.contact_card.storage.storage import ContactStorage
from app.user.user import User


class InMemoryUserStorage(ContactStorage):
    """
    Хранилище пользователей в памяти
    """
    def __init__(self):
        self._users = {}

    def get(self, user_id: int) -> User:
        return self._users.get(user_id)

    def put(self, user: User) -> int:
        self._users[user.id] = user
        return user.id
