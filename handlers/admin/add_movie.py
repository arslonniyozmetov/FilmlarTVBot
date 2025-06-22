import json, os
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states.admin_states import AddMovie
from keyboards.default.admin import admin_menu
from data.config import MOVIES_FILE

# 🎬 Kino qo‘shish
@dp.message_handler(lambda msg: msg.text == "🎬 Yangi Kino")
async def add_movie_start(message: types.Message):
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
    await message.answer("🎞 Janrini kiriting:")
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
    await message.answer("🎥 Davomiyligini kiriting:")
    await AddMovie.WaitingForDuration.set()

@dp.message_handler(state=AddMovie.WaitingForDuration)
async def add_movie_duration(message: types.Message, state: FSMContext):
    await state.update_data(duration=message.text)
    await message.answer("⭐ IMDb reytingini kiriting:")
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

    await message.answer(f"✅ Kino qo‘shildi! ID: {movie_id}", reply_markup=admin_menu())
    await state.finish()


def register_handlers(dp):
    dp.register_message_handler(add_movie_start, lambda msg: msg.text == "🎬 Yangi Kino")
    dp.register_message_handler(add_movie_video, content_types=types.ContentType.VIDEO, state=AddMovie.WaitingForMovie)
    dp.register_message_handler(add_movie_name, state=AddMovie.WaitingForName)
    dp.register_message_handler(add_movie_genre, state=AddMovie.WaitingForGenre)
    dp.register_message_handler(add_movie_language, state=AddMovie.WaitingForLanguage)
    dp.register_message_handler(add_movie_quality, state=AddMovie.WaitingForQuality)
    dp.register_message_handler(add_movie_country, state=AddMovie.WaitingForCountry)
    dp.register_message_handler(add_movie_year, state=AddMovie.WaitingForYear)
    dp.register_message_handler(add_movie_duration, state=AddMovie.WaitingForDuration)
    dp.register_message_handler(add_movie_rating, state=AddMovie.WaitingForRating)
