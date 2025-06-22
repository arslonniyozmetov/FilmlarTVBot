from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from data.config import ADMINS
from keyboards.default.admin import admin_menu
from loader import dp
from utils.misc.register_user import register_user

# START handler (bu users qismida bo'lishi kerak edi aslida)
@dp.message_handler(CommandStart())
async def admin_start(message: types.Message):
    await register_user(message.from_user)
    if message.from_user.id in ADMINS:
        await message.answer("👑 Admin panelga xush kelibsiz!", reply_markup=admin_menu())
    else:
        await message.answer("👋 Assalomu alaykum!\n\n✍🏻 Kino kodini kiriting:")