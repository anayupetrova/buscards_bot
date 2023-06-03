import uuid

from app.card_comment.card_comment import CardComment
from app.card_comment.storage.storage import CommentStorage


class InMemoryCommentStorage(CommentStorage):
    """
    Хранилище комментариев в памяти
    """
    def __init__(self):
        self._comments = {}

    def get(self, card_id: uuid.UUID, user_id: int) -> CardComment:
        return self._comments.get((card_id, user_id))

    def put(self, comment: CardComment) -> None:
        self._comments[(comment.card_id, comment.user_id)] = comment
