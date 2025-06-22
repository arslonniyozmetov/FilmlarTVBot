from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# 📄 Kinolar ro'yxati uchun sahifalash menyusi
def movies_menu(movies_slice, page, total_pages):
    keyboard = InlineKeyboardMarkup(row_width=5)
    for movie in movies_slice:
        keyboard.insert(InlineKeyboardButton(f"{movie['id']}⃣", callback_data=f"movie_{movie['id']}"))

    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("⬅", callback_data=f"movies_page_{page - 1}"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton("➡", callback_data=f"movies_page_{page + 1}"))
    if nav_buttons:
        keyboard.row(*nav_buttons)
    return keyboard


# 🎥 Kino tafsiloti tugmalari
def movie_actions_keyboard(movie_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("✏ Tahrirlash", callback_data=f"edit_{movie_id}"),
        InlineKeyboardButton("🗑 O‘chirish", callback_data=f"delete_{movie_id}"),
        InlineKeyboardButton("📊 Statistika", callback_data=f"stats_{movie_id}")
    )
    return keyboard


# ✏ Tahrirlash maydonlari
def edit_fields_keyboard(movie_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🎥 Video", callback_data=f"field_video_{movie_id}"),
        InlineKeyboardButton("🎞 Nomi", callback_data=f"field_name_{movie_id}"),
        InlineKeyboardButton("🎭 Janr", callback_data=f"field_genre_{movie_id}"),
        InlineKeyboardButton("🗣 Til", callback_data=f"field_language_{movie_id}"),
        InlineKeyboardButton("📀 Sifat", callback_data=f"field_quality_{movie_id}"),
        InlineKeyboardButton("🌏 Davlat", callback_data=f"field_country_{movie_id}"),
        InlineKeyboardButton("📆 Yil", callback_data=f"field_year_{movie_id}"),
        InlineKeyboardButton("⏳ Davomiylik", callback_data=f"field_duration_{movie_id}"),
        InlineKeyboardButton("⭐ IMDb", callback_data=f"field_rating_{movie_id}")
    )
    return keyboard
