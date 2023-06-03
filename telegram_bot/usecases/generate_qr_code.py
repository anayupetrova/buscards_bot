from pathlib import Path

import segno

from app.contact_card import ContactCard


class TelegramContactCardQRGenerator:
    """
    Класс для генерации QR-кода из контактной карточки
    """

    def __init__(self, bot_username: str):
        self._bot_username = bot_username

    def generate(self, contact_card: ContactCard, file: Path):
        """
        Генерация QR-кода из контактной карточки
        """
        card_url = f'https://t.me/{self._bot_username}?start={contact_card.id}'
        segno.make(card_url).save(str(file), dark='#0000ffcc', scale=10)
