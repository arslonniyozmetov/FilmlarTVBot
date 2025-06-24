from aiogram.types import ReplyKeyboardMarkup

def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🎬 Yangi Kino", "📡 Kanallar")
    kb.add("📁 Kinolar", "📊 Statistika")
    kb.add("👥 Obunachilar","📢 Obunachilarga xabar")
    return kb