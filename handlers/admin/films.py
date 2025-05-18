from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp
from utils.misc.is_admin import is_admin
from utils.db_api.database import add_film

class AddFilm(StatesGroup):
    waiting_for_code = State()
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_url = State()

@dp.message_handler(commands=['add_film'])
async def start_add_film(message: types.Message):
    if not is_admin(message):
        return await message.answer("⛔ Siz admin emassiz.")
    await message.answer("🎬 Kino kodi?")
    await AddFilm.waiting_for_code.set()

@dp.message_handler(state=AddFilm.waiting_for_code)
async def set_code(message: types.Message, state: FSMContext):
    await state.update_data(code=message.text)
    await message.answer("🎬 Kino nomi?")
    await AddFilm.next()

@dp.message_handler(state=AddFilm.waiting_for_title)
async def set_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("📝 Tavsif?")
    await AddFilm.next()

@dp.message_handler(state=AddFilm.waiting_for_description)
async def set_desc(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("🎥 Link?")
    await AddFilm.next()

@dp.message_handler(state=AddFilm.waiting_for_url)
async def set_url(message: types.Message, state: FSMContext):
    data = await state.get_data()
    code = data['code']
    title = data['title']
    description = data['description']
    url = message.text

    await add_film(code, title, description, url)  # bazaga qo‘shiladi
    await message.answer("✅ Kino qo‘shildi!")
    await state.finish()
