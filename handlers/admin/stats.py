from aiogram import types
from loader import dp
from data.config import ADMINS
from utils.db_api.database import get_user_count

@dp.message_handler(commands=['stats'])
async def stats_cmd(message: types.Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("Siz admin emassiz.")

    count = await get_user_count()
    await message.answer(f"👤 Foydalanuvchilar soni: {count}")
