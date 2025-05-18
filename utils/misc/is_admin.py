from aiogram.types import Message
from data.config import ADMINS

def is_admin(message: Message) -> bool:
    return message.from_user.id in ADMINS