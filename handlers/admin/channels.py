import os
import json
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from data.config import ADMINS, CHANNELS_FILE
from states.admin_states import AddChannel

# 📡 Kanallar bo‘limi
@dp.message_handler(lambda msg: msg.text == "📡 Kanallar")
async def channels_menu(message: types.Message):
    if message.from_user.id not in ADMINS:
        return

    await show_channels_menu(message)

async def show_channels_menu(message_or_callback):
    os.makedirs("data", exist_ok=True)
    data = {"channels": []}
    if os.path.exists(CHANNELS_FILE) and os.path.getsize(CHANNELS_FILE) > 0:
        with open(CHANNELS_FILE, "r") as f:
            data = json.load(f)

    text = "📄 Kanallar ro‘yxati:\n\n"
    if data.get("channels"):
        for channel in data["channels"]:
            text += f"{channel['link']}\n"
    else:
        text += "❌ Hozircha kanal yo‘q.\n"

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("➕ Qo‘shish", callback_data="add_channel"),
        InlineKeyboardButton("🗑 O‘chirish", callback_data="delete_channel_menu")
    )

    if isinstance(message_or_callback, types.Message):
        await message_or_callback.answer(text, reply_markup=keyboard)
    else:  # Callback
        await message_or_callback.message.edit_text(text, reply_markup=keyboard)

# ➕ Kanal qo‘shish
@dp.callback_query_handler(lambda c: c.data == "add_channel")
async def add_channel_start(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Kanal linkini yuboring (format: @username):")
    await AddChannel.WaitingForChannelLink.set()

@dp.message_handler(state=AddChannel.WaitingForChannelLink)
async def process_channel_link(message: types.Message, state: FSMContext):
    channel_link = message.text.strip()

    os.makedirs("data", exist_ok=True)
    data = {"channels": []}
    if os.path.exists(CHANNELS_FILE) and os.path.getsize(CHANNELS_FILE) > 0:
        with open(CHANNELS_FILE, "r") as f:
            data = json.load(f)

    channel_id = len(data["channels"]) + 1
    data["channels"].append({"id": channel_id, "link": channel_link})

    with open(CHANNELS_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await message.answer(f"✅ Kanal qo‘shildi: {channel_link}")
    await state.finish()
    await show_channels_menu(message)

# 📄 Ro'yxat yangilash
@dp.callback_query_handler(lambda c: c.data == "list_channels")
async def list_channels(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await show_channels_menu(callback_query)

# 🗑 O‘chirish menyusi
@dp.callback_query_handler(lambda c: c.data == "delete_channel_menu")
async def delete_channel_menu(callback_query: types.CallbackQuery):
    await callback_query.answer()
    if not os.path.exists(CHANNELS_FILE):
        await callback_query.message.answer("❌ Hozircha kanal yo‘q.")
        return

    with open(CHANNELS_FILE, "r") as f:
        data = json.load(f)

    if not data.get("channels"):
        await callback_query.message.answer("❌ Hozircha kanal yo‘q.")
        return

    text = "🗑 O‘chirish uchun kanalni tanlang:"
    keyboard = InlineKeyboardMarkup(row_width=1)
    for channel in data["channels"]:
        keyboard.add(
            InlineKeyboardButton(
                channel['link'],
                callback_data=f"delete_channel:{channel['id']}"
            )
        )
    keyboard.add(
        InlineKeyboardButton("🔙 Orqaga", callback_data="list_channels")
    )
    await callback_query.message.edit_text(text, reply_markup=keyboard)

# 🗑 O‘chirish amali
@dp.callback_query_handler(lambda c: c.data.startswith("delete_channel:"))
async def delete_channel(callback_query: types.CallbackQuery):
    await callback_query.answer()
    channel_id_to_delete = int(callback_query.data.split(":")[1])

    with open(CHANNELS_FILE, "r") as f:
        data = json.load(f)

    data["channels"] = [ch for ch in data["channels"] if ch["id"] != channel_id_to_delete]

    with open(CHANNELS_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await callback_query.message.answer("✅ Kanal o‘chirildi.")
    await show_channels_menu(callback_query)
