from aiogram.utils.exceptions import ChatNotFound

from data.config import ADMINS


async def on_startup_notify(dp):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Bot ishga tushdi")
        except ChatNotFound:
            print(f"Admin chat topilmadi: {admin}")
