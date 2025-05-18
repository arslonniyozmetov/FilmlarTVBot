from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from html import escape
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f"👋 Assalomu alaykum <b>{escape(message.from_user.full_name)}</b> botimizga xush kelibsiz.\n\n"
        "✍🏻 Kino kodini yuboring.",
        parse_mode="HTML"
    )
