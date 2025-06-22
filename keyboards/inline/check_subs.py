from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_subs_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("✅ Obuna bo‘ldim", callback_data="check_subs")
)