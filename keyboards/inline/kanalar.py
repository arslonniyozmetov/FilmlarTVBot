from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kanalar_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="1-kanal",
            url="https://t.me/FilmsTopChannels?start=FilmsTop01_bot"
        )
    ],
    [
        InlineKeyboardButton(
            text="2-kanal",
            url="https://t.me/Kino_Time121?start=FilmsTop01_bot"
        )
    ],
    [
        InlineKeyboardButton(text="✅Obunani tekshirish", callback_data="tekshir")
    ],
])