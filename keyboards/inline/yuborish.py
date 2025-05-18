from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

post_callback = CallbackData("post", "action")

yuborish = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Chop etish", callback_data=post_callback.new(action="yuborish")),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=post_callback.new(action="to'xtatish")),
        ]
    ]
)
