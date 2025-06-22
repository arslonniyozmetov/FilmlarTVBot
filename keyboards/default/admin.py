from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🎬 Yangi Kino", "📡 Kanallar")
    kb.add("📁 Kinolar", "📊 Statistika")
    kb.add("👥 Obunachilar","📢 Obunachilarga xabar")
    return kb
def movie_actions_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("✏ Tahrirlash", "🗑 O'chirish")
    kb.add("🚫 Bekor qilish")
    return kb
