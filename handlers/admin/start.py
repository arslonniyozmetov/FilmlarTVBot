import os
import json
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from loader import dp
from states.admin_states import AddMovie, AddChannel
from data.config import ADMINS
from keyboards.default.admin import admin_menu

USERS_FILE = 'data/users.json'
MOVIES_FILE = 'data/movies.json'
CHANNELS_FILE = 'data/channels.json'

# User registratsiya
async def register_user(user_id):
    os.makedirs("data", exist_ok=True)
    data = {"users": []}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
    if user_id not in data["users"]:
        data["users"].append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(data, f, indent=4)

# /start komandasi
@dp.message_handler(CommandStart())
async def admin_start(message: types.Message):
    await register_user(message.from_user.id)
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
@dp.message_handler(lambda msg: msg.text == "📊 Statistika")
async def statistics(message: types.Message):
    movies_count = channels_count = 0
    if os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, "r") as f:
            movies_count = len(json.load(f).get("movies", []))
    if os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, "r") as f:
            channels_count = len(json.load(f).get("channels", []))
    await message.answer(f"🎬 Kinolar: {movies_count}\n📡 Kanallar: {channels_count}")

# Obunachilar soni
@dp.message_handler(lambda msg: msg.text == "👥 Obunachilar")
async def subscribers(message: types.Message):
    users_count = 0
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users_count = len(json.load(f).get("users", []))
    await message.answer(f"👥 Obunachilar: {users_count} ta")
