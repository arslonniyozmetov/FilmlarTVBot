from aiogram import types

from filters import AdminFilter
from loader import dp
import os
import json
from datetime import datetime
from collections import Counter

USERS_FILE = 'data/users.json'
MOVIES_FILE = 'data/movies.json'
LOG_FILE = 'data/logs.json'

@dp.message_handler(AdminFilter(),lambda msg: msg.text == "📊 Statistika")
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
    # Calculate most popular
    view_counter = Counter(view["movie_id"] for view in views)

    if view_counter:
        top_movie_id = view_counter.most_common(1)[0][0]
        top_movie = next((m for m in movies if m["id"] == top_movie_id), None)
        most_popular = top_movie["name"] if top_movie else "Noma'lum"
        top_views = view_counter[top_movie_id]
        top_movie_info = f"{most_popular} ({top_views} marta, ID: {top_movie_id})"
    else:
        top_movie_info = "Ma'lumot yo'q (0 marta)"

    text = (
        "<b>📊 Statistika:</b>\n\n"
        f"🎬 <b>Jami kinolar:</b> {movies_count} ta\n"
        f"🎥 <b>Eng mashhur kino:</b> {top_movie_info}\n"
        f"👥 <b>Foydalanuvchilar:</b> {users_count} ta\n"
        f"🆕 <b>Bugun qo‘shilgan:</b> {today_count} ta"
    )

    await message.answer(text, parse_mode="HTML")


