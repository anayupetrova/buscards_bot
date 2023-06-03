import logging
import os
import re
import tempfile
import uuid
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery, ContentType, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

from app.contact_card import ContactCard
from app.usecases.get_social_network import get_social_networks
from middleware import TypingMiddleware, FSMFinishMiddleware

from app.contact_card.storage.in_memory_storage import InMemoryContactStorage
from telegram_bot.state_groups import CreateCardSG
from telegram_bot.usecases.generate_qr_code import TelegramContactCardQRGenerator
from telegram_bot.usecases.get_contact_card_message import get_contact_card_message

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(TypingMiddleware())
dp.middleware.setup(FSMFinishMiddleware(dispatcher=dp))


contacts_storage = InMemoryContactStorage()


@dp.message_handler(CommandStart())
async def start_command(message: types.Message):
    """
    Обработка команды /start, перехода по ссылке подключения и нажатия на кнопку запуска бота.
    """

    payload = message.get_args()
    if payload:
        try:
            contact_card_uuid = uuid.UUID(payload)
        except (ValueError, TypeError):
            await message.reply("Неправильный формат визитки, обратитесь к отправителю.")
            return
        contact_card = contacts_storage.get(contact_card_uuid)
        await message.reply(f"{contact_card.name} поделился с тобой визиткой.")
        card_message = get_contact_card_message(contact_card)
        await message.reply_photo(
            photo=card_message['photo'], caption=card_message['text'], reply_markup=card_message['reply_markup']
        )
    else:
        await message.reply(f"Здравствуйте!")
        await message.reply(message.from_user.id)


@dp.message_handler(commands=['create_card'])
async def create_card(message: types.Message, state: FSMContext):
    """
    Обработка команды /create_card, создание визитки.
    """

    await message.reply("Отлично! Давай создадим новую визитку. Для начала, напиши свое имя и фамилию.")
    await state.set_state(CreateCardSG.get_name)


@dp.message_handler(state=CreateCardSG.get_name)
async def get_name(message: types.Message, state: FSMContext):
    """
    Обработка имени и фамилии.
    """

    name = message.text
    await state.update_data(name=name)
    await message.reply("Как называется компания, в которой ты работаешь?")
    await state.set_state(CreateCardSG.get_company)


@dp.message_handler(state=CreateCardSG.get_company)
async def get_company(message: types.Message, state: FSMContext):
    """
    Обработка названия компании.
    """

    company = message.text
    await state.update_data(company=company)
    await message.reply("Какая у тебя должность?")
    await state.set_state(CreateCardSG.get_position)


@dp.message_handler(state=CreateCardSG.get_position)
async def get_position(message: types.Message, state: FSMContext):
    """
    Обработка должности.
    """

    position = message.text
    await state.update_data(position=position)
    await message.reply("Расскажи немного о себе.")
    await state.set_state(CreateCardSG.get_about)


@dp.message_handler(state=CreateCardSG.get_about)
async def get_about(message: types.Message, state: FSMContext):
    """
    Обработка описания.
    """

    about = message.text
    await state.update_data(about=about)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Пропустить", callback_data="skip"))
    await message.reply(
        "Хочешь оставить почту? Если да - введи ее, если нет - нажми \"Пропустить\".",
        reply_markup=keyboard
    )
    await state.set_state(CreateCardSG.get_email)


@dp.callback_query_handler(lambda c: re.match(r'^skip$', c.data), state=CreateCardSG.get_email)
async def skip_email(callback_query: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup()

    social_networks = get_social_networks()
    for social_network in social_networks.values():
        keyboard.add(InlineKeyboardButton(text=social_network, callback_data="new_link"))

    keyboard.add(InlineKeyboardButton(text="Пропустить", callback_data="skip"))

    await callback_query.message.reply(
        "Хорошо, пропустим. На какую соц.сеть ты хочешь оставить ссылку?",
        reply_markup=keyboard
    )
    await state.set_state(CreateCardSG.get_social_network)


@dp.message_handler(state=CreateCardSG.get_email)
async def get_email(message: types.Message, state: FSMContext):
    """
    Обработка почты.
    """

    email = message.text
    await state.update_data(email=email)

    keyboard = InlineKeyboardMarkup()

    social_networks = get_social_networks()
    for social_network in social_networks.values():
        keyboard.add(InlineKeyboardButton(text=social_network, callback_data="new_link"))

    keyboard.add(InlineKeyboardButton(text="Пропустить", callback_data="skip"))

    await message.reply(
        "На какую соц.сеть ты хочешь оставить ссылку?",
        reply_markup=keyboard
    )
    await state.set_state(CreateCardSG.get_social_network)


@dp.callback_query_handler(lambda c: re.match(r'^new_link$', c.data), state=CreateCardSG.get_social_network)
async def get_social_network_link(callback_query: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Пропустить", callback_data="skip"))

    await callback_query.message.reply(
        "Введи ссылку на соц.сеть.",
        reply_markup=keyboard
    )

    await state.set_state(CreateCardSG.get_social_network_link)


@dp.callback_query_handler(lambda c: re.match(r'^skip$', c.data), state=CreateCardSG.get_social_network_link)
async def skip_social_network_link(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.reply(
        "Хорошо, пропустим. Добавь фотографию к твоей визитке."
    )
    await state.set_state(CreateCardSG.get_photo)


@dp.message_handler(state=CreateCardSG.get_social_network_link)
async def get_social_network_link(message: types.Message, state: FSMContext):
    """
    Обработка ссылки на соц.сеть.
    """

    social_network_link = message.text
    state_data = await state.get_data()
    social_links = state_data.get("social_links", [])
    social_links.append(social_network_link)
    await state.update_data(social_links=social_links)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Добавить еще одну ссылку", callback_data="new_link"))
    keyboard.add(InlineKeyboardButton(text="Пропустить", callback_data="skip"))
    await message.reply(
        "Хочешь оставить еще одну ссылку?",
        reply_markup=keyboard
    )
    await state.set_state(CreateCardSG.get_social_network)


@dp.callback_query_handler(lambda c: re.match(r'^skip$', c.data), state=CreateCardSG.get_social_network)
async def skip_social_network(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.reply(
        "Хорошо, пропустим. Добавь фотографию к твоей визитке."
    )
    await state.set_state(CreateCardSG.get_photo)


@dp.message_handler(content_types=ContentType.PHOTO, state=CreateCardSG.get_photo)
async def handle_photo(message: types.Message, state: FSMContext):
    """
    Обработка фотографии.
    """

    photo_id = message.photo[-1].file_id
    await message.reply("Отлично! Твоя визитка готова!")
    state_data = await state.get_data()
    contact_card = ContactCard(
        name=state_data['name'],
        company=state_data['company'],
        position=state_data['position'],
        about=state_data['about'],
        email=state_data.get('email'),
        social_links=state_data.get('social_links', []),
        avatar_id=photo_id
    )
    contacts_storage.put(contact_card)
    card_message = get_contact_card_message(contact_card)
    await message.reply_photo(
        photo=card_message['photo'], caption=card_message['text'], reply_markup=card_message['reply_markup']
    )

    bot_info = await dp.bot.get_me()
    qr_gen = TelegramContactCardQRGenerator(bot_info.username)
    with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
        qr_gen.generate(contact_card, Path(tmp.name))
        await message.reply_photo(photo=Path(tmp.name).read_bytes())

    await state.finish()


@dp.message_handler(lambda message: message.text.startswith('/'))
async def unknown_command(message: types.Message):
    await message.reply(
        "Неизвестная команда. Помощь по командам /help."
    )


@dp.callback_query_handler(state='*')
async def unknown_handler(callback_query: CallbackQuery):
    await callback_query.message.reply(
        "Кнопка устарела. Помощь по командам /help."
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
