from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.card_comment.card_comment import CardComment
from app.contact_card import ContactCard
from app.usecases.get_social_network import get_social_network


def get_contact_card_message(contact: ContactCard, comment: Optional[CardComment]) -> dict:
    """
    Функция для формирования сообщения с контактной карточкой
    """
    message = f'Имя: {contact.name}\n'
    message += f'Компания: {contact.company}\n'
    message += f'Должность: {contact.position}\n'
    message += f'О себе: {contact.about}\n'

    if comment:
        message += f'\nКомментарий: {comment.text}\n'

    keyboard = InlineKeyboardMarkup()
    for link in contact.social_links:
        social_name = get_social_network(link) or 'Другая соц.сеть'
        keyboard.add(InlineKeyboardButton(social_name, url=link))

    keyboard.add(
        InlineKeyboardButton(
            f'{"Изменить" if comment else "Добавить"} комментарий', callback_data=f'comment_{contact.id}'
        )
    )

    return {
        'text': message,
        'reply_markup': keyboard,
        'photo': contact.avatar_id
    }
