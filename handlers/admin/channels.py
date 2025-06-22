import os
import json
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from data.config import ADMINS, CHANNELS_FILE
from states.admin_states import AddChannel

# 📡 Kanallar bo‘limi
@dp.message_handler(lambda msg: msg.text == "📡 Kanallar")
async def channels_menu(message: types.Message):
    if message.from_user.id not in ADMINS:
        return

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("➕ Qo‘shish", callback_data="add_channel"),
        InlineKeyboardButton("📄 Ro‘yxat", callback_data="list_channels")
    )
    await message.answer("📡 Kanallar bo‘limi:", reply_markup=keyboard)

# ➕ Kanal qo‘shish
@dp.callback_query_handler(lambda c: c.data == "add_channel")
async def add_channel_start(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Kanal linkini yuboring:")
    await AddChannel.WaitingForChannelLink.set()
    await callback_query.answer()

@dp.message_handler(state=AddChannel.WaitingForChannelLink)
async def process_channel_link(message: types.Message, state: FSMContext):
    channel_link = message.text.strip()

    os.makedirs("data", exist_ok=True)
    data = {"channels": []}
    if os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, "r") as f:
            data = json.load(f)

    channel_id = len(data["channels"]) + 1
    data["channels"].append({"id": channel_id, "link": channel_link})

    with open(CHANNELS_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await message.answer(f"✅ Kanal qo‘shildi. ID: {channel_id}")
    await state.finish()

# 📄 Ro'yxat ko'rsatish
@dp.callback_query_handler(lambda c: c.data == "list_channels")
async def list_channels(callback_query: types.CallbackQuery):
    if not os.path.exists(CHANNELS_FILE):
        await callback_query.message.answer("❌ Hech qanday kanal mavjud emas.")
        await callback_query.answer()
        return

    with open(CHANNELS_FILE, "r") as f:
        data = json.load(f)

    if not data.get("channels"):
        await callback_query.message.answer("❌ Hech qanday kanal mavjud emas.")
        await callback_query.answer()
        return

    text = "📄 Kanallar ro‘yxati:\n\n"
    for channel in data["channels"]:
        text += f"ID: {channel['id']} | Link: {channel['link']}\n"

    await callback_query.message.answer(text)
    await callback_query.answer()
