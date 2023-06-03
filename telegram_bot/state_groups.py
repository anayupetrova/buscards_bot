from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateCardSG(StatesGroup):
    """Группа состояний aiogram создания карточки"""
    get_name = State()
    get_company = State()
    get_position = State()
    get_about = State()
    get_email = State()
    get_social_network = State()
    get_social_network_link = State()
    get_photo = State()


class AddCardCommentSG(StatesGroup):
    """Группа состояний aiogram добавления комментария к карточке"""
    get_comment = State()
