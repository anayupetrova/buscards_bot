from app.contact_card import ContactCard
from app.user.user import User


def remove_contact(user: User, contact: ContactCard) -> bool:
    try:
        user.contact_cards.pop(user.contact_cards.index(contact))
        return True
    except IndexError:
        return False
