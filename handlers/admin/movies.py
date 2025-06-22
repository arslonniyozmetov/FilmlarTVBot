import os
import json
from collections import Counter

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.admin.statistics import LOG_FILE
from keyboards.default.admin import admin_menu
from loader import dp, bot
from data.config import ADMINS
from states.admin_states import EditMovie
from keyboards.default.admin import movie_actions_keyboard
from keyboards.inline.admin import movies_menu,  edit_fields_keyboard

MOVIES_FILE = 'data/movies.json'
LOGS_FILE = 'data/logs.json'
PAGE_SIZE = 5  # Sahifadagi kinolar soni

# 📁 Kinolar menyusi
@dp.message_handler(lambda msg: msg.text == "📁 Kinolar")
async def show_movies(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    await send_movies_page(message.chat.id, page=1)

@dp.callback_query_handler(lambda c: c.data.startswith("movies_page_"))
async def paginate_movies(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split("_")[-1])
    await send_movies_page(callback_query.message.chat.id, page)
    await callback_query.answer()

async def send_movies_page(chat_id, page=1):
    if not os.path.exists(MOVIES_FILE):
        await bot.send_message(chat_id, "❌ Hech qanday kino mavjud emas.")
        return

    with open(MOVIES_FILE, "r") as f:
        data = json.load(f)
    movies = data.get("movies", [])

    # Log fayldan ko‘rishlar sonini o‘qiymiz
    view_counter = Counter()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs_data = json.load(f)
            view_counter = Counter(view["movie_id"] for view in logs_data.get("views", []))

    total_pages = (len(movies) + PAGE_SIZE - 1) // PAGE_SIZE
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    movies_slice = movies[start:end]

    text = f"🎬 Kinolar ro'yxati ({page}/{total_pages} sahifa):\n\n"
    text += "#️⃣ ID | 🎞 Nomi       | 👁 Ko‘rishlar\n"
    text += "-----------------------------------\n"

    for film in movies_slice:
        movie_id = film['id']
        name = film['name'][:10]
        views = view_counter.get(movie_id, 0)
        text += f"{movie_id:<2} | {name:<10} | {views}\n"

    keyboard = movies_menu(movies_slice, page, total_pages)
    await bot.send_message(chat_id, text, reply_markup=keyboard)

# 📄 Kinoni tanlash
@dp.callback_query_handler(lambda c: c.data.startswith("movie_"))
async def movie_details(callback_query: types.CallbackQuery, state: FSMContext):

    movie_id = int(callback_query.data.split("_")[-1])

    with open(MOVIES_FILE, "r") as f:
        data = json.load(f)
    movie = next((m for m in data.get("movies", []) if m["id"] == movie_id), None)

    if not movie:
        await callback_query.answer("❌ Kino topilmadi.", show_alert=True)
        return

    await state.update_data(movie_id=movie_id)

    caption = (
        f"🎞 <b>{movie['name']}</b> ({movie['year']})\n"
        f"⭐ IMDb: {movie['rating']}\n"
        f"🎭 Janr: {movie['genre']}\n"
        f"🌏 Davlat: {movie['country']}\n"
        f"🗣 Til: {movie['language']}\n"
        f"📀 Sifat: {movie['quality']}\n"
        f"⏳ Davomiylik: {movie['duration']}"
    )

    keyboard = movie_actions_keyboard()
    await bot.send_video(
        chat_id=callback_query.message.chat.id,
        video=movie['file_id'],
        caption=caption,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await callback_query.answer()


@dp.message_handler(lambda msg: msg.text == "✏ Tahrirlash")
async def edit_movie_start(message: types.Message, state: FSMContext):
    data = await state.get_data()
    movie_id = data.get("movie_id")

    if not movie_id:
        await message.answer("❌ Kino tanlanmagan.")
        return

    kb = edit_fields_keyboard(movie_id)  # chaqirish
    await message.answer("✏ Qaysi maydonni tahrirlaymiz?", reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data.startswith("field_"), state="*")
async def edit_field(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split("_")
    field = data[1]
    movie_id = int(data[2])
    await state.update_data(movie_id=movie_id, edit_field=field)

    if field == "video":
        await callback_query.message.answer("🎥 Yangi video faylni yuboring:")
        await EditMovie.WaitingForVideo.set()
    else:
        field_names = {
            "name": "Kino nomi",
            "genre": "Janr",
            "language": "Til",
            "quality": "Sifat",
            "country": "Davlat",
            "year": "Yili",
            "duration": "Davomiylik",
            "rating": "IMDb reyting"
        }
        await callback_query.message.answer(f"✏ Yangi {field_names[field]} ni kiriting:")
        await EditMovie.WaitingForText.set()
    await callback_query.answer()

# Matnli maydonni saqlash
@dp.message_handler(state=EditMovie.WaitingForText)
async def save_text_field(message: types.Message, state: FSMContext):
    data = await state.get_data()
    movie_id = data.get("movie_id")
    field = data.get("edit_field")
    value = message.text.strip()

    with open(MOVIES_FILE, "r") as f:
        movies = json.load(f).get("movies", [])

    for m in movies:
        if m["id"] == movie_id:
            m[field] = value
            break

    with open(MOVIES_FILE, "w") as f:
        json.dump({"movies": movies}, f, indent=4)

    await message.answer("✅ Ma'lumot yangilandi.",reply_markup=admin_menu())
    await state.finish()

# Video faylni saqlash
@dp.message_handler(content_types=types.ContentType.VIDEO, state=EditMovie.WaitingForVideo)
async def save_video_field(message: types.Message, state: FSMContext):
    data = await state.get_data()
    movie_id = data.get("movie_id")
    file_id = message.video.file_id

    with open(MOVIES_FILE, "r") as f:
        movies = json.load(f).get("movies", [])

    for m in movies:
        if m["id"] == movie_id:
            m["file_id"] = file_id
            break

    with open(MOVIES_FILE, "w") as f:
        json.dump({"movies": movies}, f, indent=4)

    await message.answer("✅ Video yangilandi.")
    await state.finish()



@dp.message_handler(lambda msg: msg.text == "🗑 O'chirish")
async def delete_movie(message: types.Message, state: FSMContext):
    data = await state.get_data()
    movie_id = data.get("movie_id")

    if not movie_id:
        await message.answer("❌ Kino tanlanmagan.")
        return

    # Fayldan ma'lumotlarni o'qish
    with open(MOVIES_FILE, "r") as f:
        movies = json.load(f).get("movies", [])

    # O'chiriladigan kinoni ajratib olish
    movies = [m for m in movies if m["id"] != movie_id]

    # Yangilangan faylni saqlash
    with open(MOVIES_FILE, "w") as f:
        json.dump({"movies": movies}, f, indent=4)

    await message.answer("🗑 Kino o‘chirildi.", reply_markup=admin_menu())
    await state.finish()
