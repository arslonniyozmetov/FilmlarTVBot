from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data.config import ADMINS, CHANNELS
from handlers.admin.start import register_user
from keyboards.default.admin import admin_menu
from loader import dp, bot
from utils.db_api.database import get_film_by_code
from handlers.users.check_subs import check_subscription
from keyboards.inline.check_subs import check_subs_kb
from utils.misc.logger import log_movie_view


# /start komandasi
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await register_user(message.from_user.id)

    if message.from_user.id in ADMINS:
        await message.answer("👑 Admin panelga xush kelibsiz!", reply_markup=admin_menu())
    else:
        await message.answer("👋 Assalomu alaykum!\n\n✍🏻 Kino kodini kiriting:")


@dp.message_handler(lambda msg: msg.text.isdigit())
async def get_film(message: types.Message):
    user_id = message.from_user.id

    # Obuna tekshiruvi
    is_subscribed = True
    markup = InlineKeyboardMarkup(row_width=1)
    text = "Iltimos, quyidagi kanalga obuna bo‘ling:\n"

    for channel in CHANNELS:
        status = await check_subscription(bot, user_id, channel)
        if not status:
            is_subscribed = False
            chat = await bot.get_chat(channel)
            invite_link = chat.invite_link or (await chat.export_invite_link())
            markup.add(InlineKeyboardButton(chat.title, url=invite_link))

    if not is_subscribed:
        markup.inline_keyboard += check_subs_kb.inline_keyboard
        await message.answer(text, reply_markup=markup)
        return

    # Kino qidirish
    film = await get_film_by_code(message.text)
    if film:
        await log_movie_view(int(message.text), message.from_user.id)  # <-- log yozildi
        text = f"""
━━━━━━━━━━━━━━━━
🎬 *{film['title']}*

🎞 *Janr:* {film['genre']}
📆 *Yil:* {film['year']}
🌍 *Davlat:* {film['country']}
🗣 *Til:* {film['language']}
💿 *Sifat:* {film['quality']}
⏰ *Davomiylik:* {film['duration']}
⭐ *IMDb:* {film['rating']}/10
━━━━━━━━━━━━━━━━

👉 [📺 Kanalimiz](https://t.me/filmlar_kinolar_multfilmlar) | [🤖 Bot: @filmlar_tv_robot]
"""
        await message.answer_video(
            film['file_id'],
            caption=text,
            parse_mode="Markdown",
        )
    else:
        await message.answer("❌ Bunday kod bilan kino topilmadi.")





# "Obuna bo‘ldim" tugmasi uchun qayta tekshirish
@dp.callback_query_handler(lambda c: c.data == "check_subs")
async def process_check_subs(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name
    is_subscribed = True

    markup = InlineKeyboardMarkup(row_width=1)
    text = "Iltimos, quyidagi kanalga obuna bo‘ling:\n"

    for channel in CHANNELS:
        status = await check_subscription(bot, user_id, channel)
        if not status:
            is_subscribed = False
            chat = await bot.get_chat(channel)
            invite_link = chat.invite_link or (await chat.export_invite_link())
            markup.add(InlineKeyboardButton(chat.title, url=invite_link))

    markup.inline_keyboard += check_subs_kb.inline_keyboard

    await callback_query.message.delete()
    if not is_subscribed:
        await bot.send_message(user_id, text, reply_markup=markup)
    else:
        await bot.send_message(user_id, f"👋 Assalomu alaykum {user_name}. Kino kodini kiriting:")
