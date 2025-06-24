import os
import json
from collections import Counter

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import AdminFilter
from loader import dp, bot
from states.admin_states import EditMovie
from keyboards.default.admin import admin_menu
from keyboards.inline.admin import movies_menu, edit_fields_keyboard, movie_actions_keyboard

MOVIES_FILE = 'data/movies.json'
LOG_FILE = 'data/logs.json'
PAGE_SIZE = 5

# --- JSON yordamchi funksiyalar ---
def load_movies():
    if not os.path.exists(MOVIES_FILE):
        return []
    with open(MOVIES_FILE, "r") as f:
        return json.load(f).get("movies", [])

def save_movies(movies):
    with open(MOVIES_FILE, "w") as f:
        json.dump({"movies": movies}, f, indent=4)

def load_views():
    if not os.path.exists(LOG_FILE):
        return Counter()
    with open(LOG_FILE, "r") as f:
        logs = json.load(f).get("views", [])
    return Counter(view["movie_id"] for view in logs)

# --- Kinolar menyusi ---
@dp.message_handler(AdminFilter(), lambda msg: msg.text == "📁 Kinolar")
async def show_movies(message: types.Message):
    await send_movies_page(message.chat.id, page=1)

@dp.callback_query_handler(AdminFilter(), lambda c: c.data.startswith("movies_page_"))
async def paginate_movies(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split("_")[-1])
    await send_movies_page(callback_query.message.chat.id, page, callback_query.message.message_id)
    await callback_query.answer()

async def send_movies_page(chat_id, page=1, message_id=None):
    movies = load_movies()
    view_counter = load_views()

    if not movies:
        if message_id:
            await bot.edit_message_text("❌ Hech qanday kino mavjud emas.", chat_id, message_id)
        else:
            await bot.send_message(chat_id, "❌ Hech qanday kino mavjud emas.")
        return

    total_pages = (len(movies) + PAGE_SIZE - 1) // PAGE_SIZE
    page = max(1, min(page, total_pages))
    start, end = (page - 1) * PAGE_SIZE, page * PAGE_SIZE
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

    if message_id:
        await bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)
    else:
        await bot.send_message(chat_id, text, reply_markup=keyboard)

# --- Kinoni tanlash ---
@dp.callback_query_handler(AdminFilter(), lambda c: c.data.startswith("movie_"))
async def movie_details(callback_query: types.CallbackQuery, state: FSMContext):
    movie_id = int(callback_query.data.split("_")[-1])
    movies = load_movies()
    movie = next((m for m in movies if m["id"] == movie_id), None)

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

    keyboard = movie_actions_keyboard(movie_id)

    media = types.InputMediaVideo(
        media=movie['file_id'],
        caption=caption,
        parse_mode="HTML"
    )

    await callback_query.message.edit_media(
        media=media,
        reply_markup=keyboard
    )

    await callback_query.answer()

# --- Tahrirlash tugmasi (inlinega o'zgardi) ---
@dp.callback_query_handler(AdminFilter(), lambda c: c.data == "edit_movie", state="*")
async def edit_movie_start(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    movie_id = data.get("movie_id")

    if not movie_id:
        await callback_query.answer("❌ Kino tanlanmagan.", show_alert=True)
        return

    kb = edit_fields_keyboard(movie_id)
    await callback_query.message.answer("✏ Qaysi maydonni tahrirlaymiz?", reply_markup=kb)
    await callback_query.answer()

@dp.callback_query_handler(AdminFilter(), lambda c: c.data.startswith("field_"), state="*")
async def edit_field(callback_query: types.CallbackQuery, state: FSMContext):
    _, field, movie_id = callback_query.data.split("_")
    movie_id = int(movie_id)
    await state.update_data(movie_id=movie_id, edit_field=field)

    if field == "video":
        await callback_query.message.answer("🎥 Yangi video faylni yuboring:")
        await EditMovie.WaitingForVideo.set()
    else:
        field_names = {
            "name": "Kino nomi", "genre": "Janr", "language": "Til", "quality": "Sifat",
            "country": "Davlat", "year": "Yili", "duration": "Davomiylik", "rating": "IMDb reyting"
        }
        await callback_query.message.answer(f"✏ Yangi {field_names[field]} ni kiriting:")
        await EditMovie.WaitingForText.set()

    await callback_query.answer()

# --- Matnli maydon saqlash ---
@dp.message_handler(AdminFilter(), state=EditMovie.WaitingForText)
async def save_text_field(message: types.Message, state: FSMContext):
    data = await state.get_data()
    movie_id = data.get("movie_id")
    field = data.get("edit_field")
    value = message.text.strip()

    movies = load_movies()
    for m in movies:
        if m["id"] == movie_id:
            m[field] = value
            break
    save_movies(movies)

    await message.answer("✅ Ma'lumot yangilandi.", reply_markup=admin_menu())
    await state.finish()

# --- Video fayl saqlash ---
@dp.message_handler(AdminFilter(), content_types=types.ContentType.VIDEO, state=EditMovie.WaitingForVideo)
async def save_video_field(message: types.Message, state: FSMContext):
    data = await state.get_data()
    movie_id = data.get("movie_id")
    file_id = message.video.file_id

    movies = load_movies()
    for m in movies:
        if m["id"] == movie_id:
            m["file_id"] = file_id
            break
    save_movies(movies)

    await message.answer("✅ Video yangilandi.", reply_markup=admin_menu())
    await state.finish()

# --- O'chirish tugmasi (inlinega o'zgardi) ---
@dp.callback_query_handler(AdminFilter(), lambda c: c.data.startswith("delete_movie_"), state="*")
async def delete_movie(callback_query: types.CallbackQuery, state: FSMContext):
    # callback_data: delete_movie_123
    movie_id_str = callback_query.data.split("_")[-1]

    try:
        movie_id = int(movie_id_str)
    except ValueError:
        await callback_query.answer("❌ Xatolik: noto'g'ri kino ID", show_alert=True)
        return

    # Fayldan ma'lumotlarni o'qish
    if not os.path.exists(MOVIES_FILE):
        await callback_query.answer("❌ Kino bazasi topilmadi.", show_alert=True)
        return

    with open(MOVIES_FILE, "r") as f:
        movies = json.load(f).get("movies", [])

    # O'chirish
    movies = [m for m in movies if m["id"] != movie_id]

    with open(MOVIES_FILE, "w") as f:
        json.dump({"movies": movies}, f, indent=4)

    await state.finish()
    await callback_query.message.delete()  # eski video xabarini o'chirish
    await callback_query.message.answer("🗑 Kino o‘chirildi.", reply_markup=admin_menu())
    await callback_query.answer()


@dp.callback_query_handler(AdminFilter(), lambda c: c.data == "back_to_movie", state="*")
async def back_to_movie_details(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    movie_id = data.get("movie_id")

    if not movie_id:
        await callback_query.answer("❌ Kino topilmadi.", show_alert=True)
        return

    movies = load_movies()
    movie = next((m for m in movies if m["id"] == movie_id), None)
    if not movie:
        await callback_query.answer("❌ Kino topilmadi.", show_alert=True)
        return

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

    media = types.InputMediaVideo(
        media=movie['file_id'],
        caption=caption,
        parse_mode="HTML"
    )

    await callback_query.message.edit_media(
        media=media,
        reply_markup=keyboard
    )

    await callback_query.message.delete()  # Eski tahrirlash oynasini o'chiramiz
    await callback_query.answer()

@dp.callback_query_handler(AdminFilter(), lambda c: c.data == "cancel_editing", state="*")
async def cancel_editing(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()

    # Inline tugmachani olib tashlaymiz
    try:
        await callback_query.message.delete()  # Butun video postini o'chirish
    except:
        pass

    # Kinolar ro'yxatini qaytadan chiqaramiz
    await send_movies_page(callback_query.message.chat.id, page=1)

