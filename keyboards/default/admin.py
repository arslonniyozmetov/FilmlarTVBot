from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🎬 Yangi Kino", "📡 Kanallar")
    kb.add("📁 Kinolar", "📊 Statistika", "👥 Obunachilar")
    return kb
