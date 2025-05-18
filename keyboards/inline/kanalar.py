from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kanalar_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="1-kanal",
            url="https://t.me/filmlar_kinolar_multfilmlar"
        )
    ],
    [
        InlineKeyboardButton(text="✅Obunani tekshirish", callback_data="tekshir")
    ],
])