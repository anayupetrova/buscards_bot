from app.contact_card import ContactCard
from app.contact_card.storage.in_memory_storage import InMemoryContactStorage
from telegram_bot.usecases.generate_qr_code import TelegramContactCardQRGenerator

if __name__ == '__main__':
    cs = InMemoryContactStorage()
    c_uuid = cs.put(
        ContactCard(
            name='Иванов Иван Иванович',
            company='ООО "Рога и копыта"',
            position='Директор',
            about='Очень хороший человек',
            social_links=['https://vk.com/ivanov', 'https://facebook.com/ivanov'],
        )
    )
    card = cs.get(c_uuid)
    print(card)
    qr_gen = TelegramContactCardQRGenerator('sslane_bot')
    qr_code = qr_gen.generate(card)
    print(qr_code)
