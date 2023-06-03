import uuid
from abc import ABC

from app.contact_card.user.user import User


class UserStorage(ABC):
    """
    Абстрактный класс хранилища пользователей
    """
    def get(self, user_id: int) -> User:
        """
        Получение контакта из хранилища
        """
        pass

    def put(self, user: User) -> int:
        """
        Добавление контакта в хранилище
        """
        pass
