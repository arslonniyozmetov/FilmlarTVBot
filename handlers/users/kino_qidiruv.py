from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp, db  # loader.py da `dp` va `db` import qilingan deb olinadi
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from states.kino_qidiruv import KinoQidiruv
from aiogram.dispatcher.filters import Text


@dp.message_handler(Command('cancel'), state=KinoQidiruv.waiting_for_kino_id)
async def cancel_kino_search(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🔴 Kino qidiruv bekor qilindi.")


@dp.message_handler(state=KinoQidiruv.waiting_for_kino_id)
async def get_kino_by_id_handler(message: types.Message, state: FSMContext):
    kino_id_text = message.text

    if not kino_id_text.isdigit():
        await message.delete()
        await message.answer(
            "❗ Iltimos, faqat raqam kiriting. Masalan: 5\n Yoki kino qidiruvni bekor qilmoqchi bo‘lsangiz '/cancel' yozing.")
        return

    kino_id = int(kino_id_text)
    kino = await db.get_kino_by_id(kino_id)

    if not kino:
        await message.answer("❌ Bu ID bo‘yicha kino topilmadi.")
        return

    caption = f"🆔 Kodi: {kino_id_text}"
    await message.answer_video(video=kino["kino_file_id"], caption=caption)

    # await state.finish()


async def qidir_kino(message: types.Message, state: FSMContext):
    # Foydalanuvchi yuborgan kino ID'sini olish
    data = await state.get_data()
    kino_id_text = data.get("kino_id_text")

    if not kino_id_text or not kino_id_text.isdigit():
        await message.answer("❌ Kino ID noto‘g‘ri.")
        return

    kino_id = int(kino_id_text)

    # Kino ma'lumotlarini bazadan olish
    kino = await db.get_kino_by_id(kino_id)

    if not kino:
        await message.answer("❌ Bu ID bo‘yicha kino topilmadi.")
        return

    # Kino haqida ma'lumotni yuborish
    caption = f"🆔 Kodi: {kino_id_text}"
    await message.answer_video(video=kino["kino_file_id"], caption=caption)