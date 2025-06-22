import os
import json
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards.inline.admin import *
from loader import dp, bot
from states.admin_states import AddMovie, AddChannel
from data.config import ADMINS
from keyboards.default.admin import admin_menu
import os
import json
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from data.config import MOVIES_FILE, ADMINS
from states.admin_states import EditMovie

USERS_FILE = 'data/users.json'
MOVIES_FILE = 'data/movies.json'
CHANNELS_FILE = 'data/channels.json'

# User registratsiya
from datetime import datetime

USERS_FILE = 'data/users.json'

from datetime import datetime

async def register_user(user: types.User):
    os.makedirs("data", exist_ok=True)
    data = {"users": []}

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            data = json.load(f)

    # Agar foydalanuvchi mavjud bo'lmasa, yangi qo'shamiz
    if not any(u['user_id'] == user.id for u in data["users"]):
        user_data = {
            "user_id": user.id,
            "first_name": user.first_name,
            "username": user.username or "",
            "register_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Sana + vaqt
        }
        data["users"].append(user_data)

        with open(USERS_FILE, "w") as f:
            json.dump(data, f, indent=4)





# /start komandasi
@dp.message_handler(CommandStart())
async def admin_start(message: types.Message):
    await register_user(message.from_user)
    if message.from_user.id in ADMINS:
        await message.answer("👑 Admin panelga xush kelibsiz!", reply_markup=admin_menu())
    else:
        await message.answer("👋 Assalomu alaykum!\n\n✍🏻 Kino kodini kiriting:")

# Admin kino qo‘shish
@dp.message_handler(lambda msg: msg.text == "🎬 Yangi Kino")
async def add_movie_start(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    await message.answer("🎞 Kino videosini yuboring:")
    await AddMovie.WaitingForMovie.set()

@dp.message_handler(content_types=types.ContentType.VIDEO, state=AddMovie.WaitingForMovie)
async def add_movie_video(message: types.Message, state: FSMContext):
    await state.update_data(file_id=message.video.file_id)
    await message.answer("🎬 Kino nomini kiriting:")
    await AddMovie.WaitingForName.set()

@dp.message_handler(state=AddMovie.WaitingForName)
async def add_movie_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🎞 Janrini kiriting (masalan: Action, Sci-Fi):")
    await AddMovie.WaitingForGenre.set()

@dp.message_handler(state=AddMovie.WaitingForGenre)
async def add_movie_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer("🗣 Tilini kiriting:")
    await AddMovie.WaitingForLanguage.set()

@dp.message_handler(state=AddMovie.WaitingForLanguage)
async def add_movie_language(message: types.Message, state: FSMContext):
    await state.update_data(language=message.text)
    await message.answer("📀 Sifatini kiriting (HD, FullHD):")
    await AddMovie.WaitingForQuality.set()

@dp.message_handler(state=AddMovie.WaitingForQuality)
async def add_movie_quality(message: types.Message, state: FSMContext):
    await state.update_data(quality=message.text)
    await message.answer("🌏 Davlatini kiriting:")
    await AddMovie.WaitingForCountry.set()

@dp.message_handler(state=AddMovie.WaitingForCountry)
async def add_movie_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await message.answer("📆 Yilini kiriting (masalan: 2023):")
    await AddMovie.WaitingForYear.set()

@dp.message_handler(state=AddMovie.WaitingForYear)
async def add_movie_year(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Faqat raqam kiriting!")
        return
    await state.update_data(year=message.text)
    await message.answer("🎥 Davomiyligini kiriting (masalan: 2 soat 45 daqiqa):")
    await AddMovie.WaitingForDuration.set()

@dp.message_handler(state=AddMovie.WaitingForDuration)
async def add_movie_duration(message: types.Message, state: FSMContext):
    await state.update_data(duration=message.text)
    await message.answer("⭐ IMDb reytingini kiriting (masalan: 8.2):")
    await AddMovie.WaitingForRating.set()

@dp.message_handler(state=AddMovie.WaitingForRating)
async def add_movie_rating(message: types.Message, state: FSMContext):
    await state.update_data(rating=message.text)

    movie_data = await state.get_data()

    os.makedirs("data", exist_ok=True)
    movies = {"movies": []}
    if os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, "r") as f:
            movies = json.load(f)

    movie_id = len(movies["movies"]) + 1
    movie_data["id"] = movie_id
    movies["movies"].append(movie_data)

    with open(MOVIES_FILE, "w") as f:
        json.dump(movies, f, indent=4)

    await message.answer(f"Kino muvaffaqiyatli qo‘shildi! ID: {movie_id}")
    await state.finish()
    await message.answer("Admin menyuga qaytdingiz.", reply_markup=admin_menu())


# Kanallar bilan ishlash
@dp.message_handler(lambda msg: msg.text == "📡 Yangi Kanal")
async def add_channel_start(message: types.Message):
    await message.answer("Kanal linkini yuboring:")
    await AddChannel.WaitingForChannelLink.set()

@dp.message_handler(state=AddChannel.WaitingForChannelLink)
async def add_channel_link(message: types.Message, state: FSMContext):
    channel_link = message.text.strip()

    os.makedirs("data", exist_ok=True)
    channels = {"channels": []}
    if os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, "r") as f:
            channels = json.load(f)

    channel_id = len(channels["channels"]) + 1
    channels["channels"].append({"id": channel_id, "link": channel_link})

    with open(CHANNELS_FILE, "w") as f:
        json.dump(channels, f, indent=4)

    await message.answer(f"Kanal qo‘shildi. ID: {channel_id}")
    await state.finish()
    await message.answer("Admin menyuga qaytdingiz.", reply_markup=admin_menu())


# Statistika
from aiogram import types
from loader import dp
import os
import json
from datetime import datetime
from collections import Counter

USERS_FILE = 'data/users.json'
MOVIES_FILE = 'data/movies.json'
LOG_FILE = 'data/logs.json'

@dp.message_handler(lambda msg: msg.text == "📊 Statistika")
async def statistics(message: types.Message):
    # Users
    users_count = today_count = 0
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f).get("users", [])
            users_count = len(users)
            today = datetime.now().strftime("%Y-%m-%d")
            today_count = sum(
                1 for user in users
                if user.get("register_date", "").startswith(today)
            )

    # Movies
    movies_count = 0
    movies = []
    if os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, "r") as f:
            movies = json.load(f).get("movies", [])
            movies_count = len(movies)

    # Log
    views = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            views = json.load(f).get("views", [])

    # Calculate most popular
    view_counter = Counter(view["movie_id"] for view in views)
    if view_counter:
        top_movie_id = view_counter.most_common(1)[0][0]
        top_movie = next((m for m in movies if m["id"] == top_movie_id), None)
        most_popular = top_movie["name"] if top_movie else "Noma'lum"
        top_views = view_counter[top_movie_id]
    else:
        most_popular = "Ma'lumot yo'q"
        top_views = 0

    text = (
        "<b>📊 Statistika:</b>\n\n"
        f"🎬 <b>Jami kinolar:</b> {movies_count} ta\n"
        f"🎥 <b>Eng mashhur kino:</b> {most_popular} ({top_views} marta)\n"
        f"👥 <b>Foydalanuvchilar:</b> {users_count} ta\n"
        f"🆕 <b>Bugun qo‘shilgan:</b> {today_count} ta"
    )

    await message.answer(text, parse_mode="HTML")



# Obunachilar soni
import json
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
        await bot.send_message(chat_id, "❌ Hech qanday foydalanuvchi mavjud emas.")
        return

    with open(USERS_FILE, "r") as f:
        data = json.load(f)

    users = data.get("users", [])
    total_pages = (len(users) + PAGE_SIZE - 1) // PAGE_SIZE

    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    users_slice = users[start:end]

    text = f"👥 Obunachilar ro‘yxati (Sahifa {page}/{total_pages}):\n\n"

    for i, user in enumerate(users_slice, start=start + 1):
        username = f"@{user.get('username', '')}" if user.get('username') else "(username yo‘q)"
        register_date = user.get("register_date", "Noma’lum sana")
        text += (
            f"{i}. {user.get('first_name', '')} {username}\n"
            f"📅 Botga qo‘shilgan: {register_date}\n\n"
        )

    keyboard = InlineKeyboardMarkup(row_width=2)
    if page > 1:
        keyboard.insert(InlineKeyboardButton("⬅ Oldingi", callback_data=f"subscribers_page_{page-1}"))
    if page < total_pages:
        keyboard.insert(InlineKeyboardButton("⏭ Keyingi", callback_data=f"subscribers_page_{page+1}"))

    await bot.send_message(chat_id, text, reply_markup=keyboard)

import os
import json
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from data.config import ADMINS
from states.admin_states import EditMovie
from keyboards.inline.admin import movies_menu, movie_actions_keyboard, edit_fields_keyboard

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

    total_pages = (len(movies) + PAGE_SIZE - 1) // PAGE_SIZE
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    movies_slice = movies[start:end]

    text = f"🎬 Kinolar ro'yxati ({page}/{total_pages} sahifa):\n\n"
    for movie in movies_slice:
        text += f"{movie['id']}⃣ {movie['name']} ({movie['year']}) ⭐ {movie['rating']}\n"

    keyboard = movies_menu(movies_slice, page, total_pages)
    await bot.send_message(chat_id, text, reply_markup=keyboard)

# 📄 Kinoni tanlash
@dp.callback_query_handler(lambda c: c.data.startswith("movie_"))
async def movie_details(callback_query: types.CallbackQuery):
    movie_id = int(callback_query.data.split("_")[-1])

    with open(MOVIES_FILE, "r") as f:
        data = json.load(f)
    movie = next((m for m in data.get("movies", []) if m["id"] == movie_id), None)

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

    keyboard = movie_actions_keyboard(movie_id)
    await bot.send_video(
        chat_id=callback_query.message.chat.id,
        video=movie['file_id'],
        caption=caption,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await callback_query.answer()

# ✏ Tahrirlash tugmasi
@dp.callback_query_handler(lambda c: c.data.startswith("edit_"))
async def edit_movie_start(callback_query: types.CallbackQuery, state: FSMContext):
    movie_id = int(callback_query.data.split("_")[-1])
    await state.update_data(movie_id=movie_id)
    keyboard = edit_fields_keyboard(movie_id)
    await callback_query.message.answer("✏ Qaysi maydonni tahrirlaymiz?", reply_markup=keyboard)
    await callback_query.answer()

# Maydon tanlash
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

    await message.answer("✅ Ma'lumot yangilandi.")
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

# 🗑 O'chirish
@dp.callback_query_handler(lambda c: c.data.startswith("delete_"))
async def delete_movie(callback_query: types.CallbackQuery):
    movie_id = int(callback_query.data.split("_")[-1])

    with open(MOVIES_FILE, "r") as f:
        movies = json.load(f).get("movies", [])

    movies = [m for m in movies if m["id"] != movie_id]

    with open(MOVIES_FILE, "w") as f:
        json.dump({"movies": movies}, f, indent=4)

    await callback_query.message.answer("🗑 Kino o‘chirildi.")
    await callback_query.answer()

# 📊 Statistika
@dp.callback_query_handler(lambda c: c.data.startswith("stats_"))
async def show_movie_stats(callback_query: types.CallbackQuery):
    movie_id = int(callback_query.data.split("_")[-1])

    if not os.path.exists(LOGS_FILE):
        await callback_query.answer("📊 Statistika mavjud emas.", show_alert=True)
        return

    with open(LOGS_FILE, "r") as f:
        logs = json.load(f).get("views", [])

    views_count = sum(1 for view in logs if view["movie_id"] == movie_id)

    await callback_query.answer(f"👁 {views_count} marta ko‘rilgan.", show_alert=True)

