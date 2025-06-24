import os
import json
import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup

from filters import AdminFilter
from loader import dp, bot
from data.config import ADMINS
from keyboards.default.admin import admin_menu

USERS_FILE = 'data/users.json'

# State lar
class BroadcastState(StatesGroup):
    WaitingForMessage = State()
    Confirming = State()

# Tugma bosilganda (xabar yuborish boshlanishi)
@dp.message_handler(AdminFilter(),lambda msg: msg.text == "📢 Obunachilarga xabar")
async def ask_broadcast_content(message: types.Message, state: FSMContext):

    cancel_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_kb.add("🚫 Bekor qilish")

    await message.answer(
        "📤 Yubormoqchi bo‘lgan xabar (matn, rasm, video, fayl...) ni jo‘nating:",
        reply_markup=cancel_kb
    )
    await BroadcastState.WaitingForMessage.set()

# Bekor qilish tugmasi (har qanday state da ishlaydi)
@dp.message_handler(AdminFilter(), lambda msg: msg.text == "🚫 Bekor qilish", state="*")
async def cancel_broadcast(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("❌ Jarayon bekor qilindi.", reply_markup=admin_menu())

# Xabar qabul qilish va tasdiqlash bosqichi
@dp.message_handler(content_types=types.ContentType.ANY, state=BroadcastState.WaitingForMessage)
async def confirm_broadcast(message: types.Message, state: FSMContext):
    await state.update_data(
        content_type=message.content_type,
        message_id=message.message_id,
        chat_id=message.chat.id
    )

    # Reply keyboardni olib tashlaymiz
    await message.answer("✅ Xabar qabul qilindi.", reply_markup=ReplyKeyboardRemove())

    # Inline tasdiqlash tugmalari
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Tasdiqlayman", callback_data="broadcast_confirm"),
        types.InlineKeyboardButton("🚫 Bekor qilish", callback_data="broadcast_cancel")
    )

    await message.answer("❓ Ushbu xabarni yuborishni tasdiqlaysizmi?", reply_markup=kb)
    await BroadcastState.Confirming.set()

# Tasdiqlash tugmasi bosilganda
@dp.callback_query_handler(lambda c: c.data == "broadcast_confirm", state=BroadcastState.Confirming)
async def send_broadcast(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()

    data = await state.get_data()
    content_type = data.get("content_type")
    message_id = data.get("message_id")
    chat_id = data.get("chat_id")

    if not os.path.exists(USERS_FILE):
        await callback_query.message.answer("❌ Foydalanuvchilar topilmadi.", reply_markup=admin_menu())
        await state.finish()
        return

    with open(USERS_FILE, "r") as f:
        users = json.load(f).get("users", [])

    count = 0
    for user in users:
        user_id = user.get("user_id")
        try:
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=chat_id,
                message_id=message_id
            )
            count += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            print(f"❌ {user_id} ga jo‘natilmadi: {e}")

    await callback_query.message.answer(
        f"✅ Xabar {count} ta foydalanuvchiga yuborildi.", reply_markup=admin_menu())
    await state.finish()

# Bekor qilish inline tugmasi bosilganda
@dp.callback_query_handler(lambda c: c.data == "broadcast_cancel", state=BroadcastState.Confirming)
async def cancel_broadcast_confirm(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer("❌ Xabar yuborish bekor qilindi.", reply_markup=admin_menu())
    await state.finish()
