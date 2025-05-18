from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎬 Kino qo'shish"),
            KeyboardButton(text="📊 Statistikani ko'rish")
        ],
        [
            KeyboardButton(text="📋 Kinolar ro'yxati"),
            KeyboardButton(text="🔙 Orqaga")
        ]
    ],
    resize_keyboard=True
)