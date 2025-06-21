import aiogram
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from keyboards.inline.check_subs import *
from loader import dp, bot
from utils.db_api.database import get_film_by_code
from utils.misc.check_subs import check_subscription
from data.config import CHANNELS

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Assalomu alaykum! 👋\nIltimos, kino kodini kiriting:")

@dp.message_handler(lambda message: message.text.isdigit())
async def get_film(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = True
    text = "Iltimos, quyidagi kanalga obuna bo'ling:\n"
    markup = InlineKeyboardMarkup()

    for channel in CHANNELS:
        status = await check_subscription(bot, user_id, channel)
        if not status:
            is_subscribed = False
            chat = await bot.get_chat(channel)
            invite_link = chat.invite_link or (await chat.export_invite_link())
            markup.add(InlineKeyboardButton(text=chat.title, url=invite_link))

    if not is_subscribed:
        markup.add(InlineKeyboardButton("✅ Obuna bo‘ldim", callback_data="check_subs"))
        await message.answer(text, reply_markup=markup)
        return

    film = await get_film_by_code(message.text)
    if film:
        await message.answer(
            f"🎬 Kino: {film['title']}\n📝 Tavsif: {film['description']}\n🎥 Link: {film['url']}"
        )
    else:
        await message.answer("❌ Bunday kodga ega kino topilmadi.")

import json

@dp.callback_query_handler(lambda c: c.data == "check_subs")
async def process_check_subs(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name
    is_subscribed = True

    text = "Iltimos, quyidagi kanalga obuna bo'ling:\n"
    markup = InlineKeyboardMarkup(row_width=1)

    for channel in CHANNELS:
        status = await check_subscription(bot, user_id, channel)
        if not status:
            is_subscribed = False
            chat = await bot.get_chat(channel)
            invite_link = chat.invite_link or (await chat.export_invite_link())
            markup.add(InlineKeyboardButton(text=chat.title, url=invite_link))

    # Doimiy tugmani oxiriga qo‘shamiz
    markup.inline_keyboard += check_subs_kb.inline_keyboard

    if not is_subscribed:
        # ❌ Obuna bo‘lmaganlar uchun: eski xabarni o‘chiramiz, yangisini yuboramiz
        await callback_query.message.delete()
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup)
    else:
        # ✅ Obuna bo‘lgan: xabarni o‘chirib, yangi welcome xabarini yuboramiz
        await callback_query.message.delete()
        welcome_text = f"👋 Assalomu alaykum {user_name} botimizga xush kelibsiz.\n\n✍🏻 Kino kodini yuboring."
        await bot.send_message(chat_id=user_id, text=welcome_text)

