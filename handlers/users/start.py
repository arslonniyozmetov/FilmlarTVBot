from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

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

@dp.callback_query_handler(lambda c: c.data == "check_subs")
async def process_check_subs(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
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

    markup.add(InlineKeyboardButton("✅ Obuna bo‘ldim", callback_data="check_subs"))

    if not is_subscribed:
        old_text = callback_query.message.text
        old_markup = callback_query.message.reply_markup

        if old_text != text or old_markup != markup:
            await callback_query.message.edit_text(text, reply_markup=markup)
        else:
            await callback_query.answer("Siz hali kanalga obuna bo‘lmadingiz!", show_alert=True)
    else:
        await callback_query.answer("Obunangiz tasdiqlandi! 🎉", show_alert=True)
        await callback_query.message.edit_text("Assalomu alaykum! 👋\nIltimos, kino kodini kiriting:")
