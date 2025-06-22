from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def movies_menu(movies_slice, page, total_pages):
    kb = InlineKeyboardMarkup(row_width=5)
    for movie in movies_slice:
        kb.insert(InlineKeyboardButton(str(movie['id']), callback_data=f"movie_{movie['id']}"))
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("⬅", callback_data=f"movies_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton("➡", callback_data=f"movies_page_{page+1}"))
    kb.row(*nav_buttons)
    return kb

def movie_actions_keyboard(movie_id):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✏ Tahrirlash", callback_data=f"edit_{movie_id}"),
        InlineKeyboardButton("🗑 O'chirish", callback_data=f"delete_{movie_id}")
    )
    kb.add(
        InlineKeyboardButton("📊 Ko'rishlar", callback_data=f"stats_{movie_id}")
    )
    return kb

def edit_fields_keyboard(movie_id):
    kb = InlineKeyboardMarkup(row_width=2)
    fields = ["name", "genre", "language", "quality", "country", "year", "duration", "rating", "video"]
    field_names = {
        "name": "Nomi", "genre": "Janr", "language": "Til", "quality": "Sifat",
        "country": "Davlat", "year": "Yil", "duration": "Davomiylik",
        "rating": "IMDb", "video": "Video"
    }
    for field in fields:
        kb.insert(InlineKeyboardButton(field_names[field], callback_data=f"field_{field}_{movie_id}"))
    return kb
