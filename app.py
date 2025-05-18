from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
# from middlewares.obuna import BigBrother  # ⬅️ middleware faylingdan import qil


async def on_startup(dispatcher):
    await db.create()
    # await db.drop_user()
    # Birlamchi komandalar (/star va /help)
    await db.create_table_users()
    await set_default_commands(dispatcher)
    # 🔒 Middleware ulash
    # dispatcher.middleware.setup(BigBrother())
    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
