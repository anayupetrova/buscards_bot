from pydantic import BaseModel


class SimpleMessage(BaseModel):
    """
    Класс-dto простого сообщения
    Содержит в себе:
        - Текст сообщения
        - Клавиатуру
        - id фото
    """
    text: str
    reply_markup: InlineKeyboardMarkup
    photo_file_id: str
