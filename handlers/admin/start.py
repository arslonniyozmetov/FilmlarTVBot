from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from loader import dp
from keyboards.default.admin import admin_start_keyboard  # Admin uchun tayyorlagan klaviaturangiz
from data.config import ADMINS


@dp.message_handler(CommandStart())
async def admin_start(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        await message.answer(
            "Assalomu alaykum, Admin! 👋\nBu yerda siz admin funksiyalarini boshqarishingiz mumkin.",
            reply_markup=admin_start_keyboard
        )
    else:
        await message.answer("Siz admin emassiz!")
