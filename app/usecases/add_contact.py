from app.contact_card import ContactCard
from app.user.user import User


def add_contact(user: User, contact: ContactCard) -> None:
    user.contact_cards.append(contact)
