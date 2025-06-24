from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data.config import ADMINS

class AdminFilter(BoundFilter):
    async def check(self, obj):
        if isinstance(obj, types.Message):
            user_id = obj.from_user.id
        elif isinstance(obj, types.CallbackQuery):
            user_id = obj.from_user.id
        else:
            return False
        return user_id in ADMINS
