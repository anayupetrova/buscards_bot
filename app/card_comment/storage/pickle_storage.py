import pickle
import uuid
from pathlib import Path

from app.card_comment.card_comment import CardComment
from app.card_comment.storage.storage import CommentStorage


class PickleCommentStorage(CommentStorage):
    """
    Хранилище комментариев в памяти
    """
    def __init__(self):
        self._comments = {}
        Path('db').mkdir(exist_ok=True)
        self._pickle_file = Path('db') / 'comments.pickle'
        self.load_from_pickle()

    def load_from_pickle(self):
        if not self._pickle_file.exists():
            self.save_to_pickle()
            return

        with self._pickle_file.open('rb') as f:
            self._comments = pickle.load(f)

    def save_to_pickle(self):
        with self._pickle_file.open('wb') as f:
            pickle.dump(self._comments, f)

    def get(self, card_id: uuid.UUID, user_id: int) -> CardComment:
        return self._comments.get((card_id, user_id))

    def put(self, comment: CardComment) -> None:
        self._comments[(comment.card_id, comment.user_id)] = comment
        self.save_to_pickle()

