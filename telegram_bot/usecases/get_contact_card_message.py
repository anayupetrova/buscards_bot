from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.contact_card import ContactCard
from app.usecases.get_social_network import get_social_network


def get_contact_card_message(contact: ContactCard) -> dict:
    """
    Функция для формирования сообщения с контактной карточкой
    """
    message = f'Имя: {contact.name}\n'
    message += f'Компания: {contact.company}\n'
    message += f'Должность: {contact.position}\n'
    message += f'О себе: {contact.about}\n'

    keyboard = InlineKeyboardMarkup()
    for link in contact.social_links:
        social_name = get_social_network(link) or 'Другая соц.сеть'
        keyboard.add(InlineKeyboardButton(social_name, url=link))

    return {
        'text': message,
        'reply_markup': keyboard,
        'photo': contact.avatar_id
    }
