import uuid
from abc import ABC

from app.card_comment.card_comment import CardComment


class CommentStorage(ABC):
    """
    Абстрактный класс хранилища комментариев
    """
    def get(self, card_id: uuid.UUID, user_id: int) -> CardComment:
        """
        Получение комментария из хранилища
        """
        pass

    def put(self, comment: CardComment) -> None:
        """
        Добавление комментария в хранилище
        """
        pass
