from aiogram import types

def admin_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🎬 Yangi Kino", "📡 Yangi Kanal")
    keyboard.add("📁 Kinolar", "📺 Kanallar")
    keyboard.add("📊 Statistika")
    keyboard.add("👥 Obunachilar")
    return keyboard

