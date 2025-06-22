import json, os
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from data.config import USERS_FILE

PAGE_SIZE = 20

@dp.message_handler(lambda msg: msg.text == "👥 Obunachilar")
async def subscribers(message: types.Message):
    await send_subscribers_page(message.chat.id, page=1)

@dp.callback_query_handler(lambda c: c.data.startswith("subscribers_page_"))
async def paginate_subscribers(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split("_")[-1])
    await send_subscribers_page(callback_query.message.chat.id, page)
    await callback_query.answer()

async def send_subscribers_page(chat_id, page=1):
    if not os.path.exists(USERS_FILE):
        await dp.bot.send_message(chat_id, "❌ Hech qanday foydalanuvchi mavjud emas.")
        return

    with open(USERS_FILE, "r") as f:
        users = json.load(f).get("users", [])

    total_pages = (len(users) + PAGE_SIZE - 1) // PAGE_SIZE
    start, end = (page-1) * PAGE_SIZE, page * PAGE_SIZE
    users_slice = users[start:end]

    text = f"👥 Obunachilar (Sahifa {page}/{total_pages}):\n\n"
    for i, user in enumerate(users_slice, start=start + 1):
        username = f"@{user['username']}" if user['username'] else "(username yo'q)"
        text += f"{i}. {user['first_name']} {username}\n📅 {user['register_date']}\n\n"

    kb = InlineKeyboardMarkup(row_width=2)
    if page > 1:
        kb.insert(InlineKeyboardButton("⬅ Oldingi", callback_data=f"subscribers_page_{page-1}"))
    if page < total_pages:
        kb.insert(InlineKeyboardButton("➡ Keyingi", callback_data=f"subscribers_page_{page+1}"))

    await dp.bot.send_message(chat_id, text, reply_markup=kb)

