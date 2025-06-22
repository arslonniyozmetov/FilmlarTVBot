# handlers/admin/broadcast.py

import os
import json
import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from data.config import ADMINS
from keyboards.default.admin import admin_menu

USERS_FILE = 'data/users.json'

from aiogram.dispatcher.filters.state import State, StatesGroup


class BroadcastState(StatesGroup):
    WaitingForMessage = State()


# Tugma bosilganda
@dp.message_handler(lambda msg: msg.text == "📢 Obunachilarga xabar")
async def ask_broadcast_content(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return await message.answer("⛔ Siz admin emassiz.")

    cancel_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_kb.add("🚫 Bekor qilish")

    await message.answer("📤 Yubormoqchi bo‘lgan xabar (matn, rasm, video, fayl...) ni jo‘nating:",
                         reply_markup=cancel_kb)
    await BroadcastState.WaitingForMessage.set()


# Bekor qilish tugmasi
@dp.message_handler(lambda msg: msg.text == "🚫 Bekor qilish", state=BroadcastState.WaitingForMessage)
async def cancel_broadcast(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("❌ Bekor qilindi.", reply_markup=admin_menu)


# Xabarni qabul qilish va tarqatish
@dp.message_handler(content_types=types.ContentType.ANY, state=BroadcastState.WaitingForMessage)
async def start_broadcast(message: types.Message, state: FSMContext):
    await state.finish()

    if not os.path.exists(USERS_FILE):
        return await message.answer("❌ Foydalanuvchilar topilmadi.", reply_markup=admin_menu)

    with open(USERS_FILE, "r") as f:
        users = json.load(f).get("users", [])

    count = 0
    for user in users:
        user_id = user.get("user_id")
        try:
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            count += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            print(f"❌ {user_id} ga jo‘natilmadi: {e}")

    await message.answer(f"✅ Xabar {count} ta foydalanuvchiga yuborildi.", reply_markup=admin_menu())
    return None
