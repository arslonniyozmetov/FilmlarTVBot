# from aiogram import types
# from aiogram.dispatcher.handler import CancelHandler
# from aiogram.dispatcher.middlewares import BaseMiddleware
# from utils.misc import obuna
# from loader import bot
# from data.config import CHANNELS
# from keyboards.inline.kanalar import kanalar_button
#
#
# class BigBrother(BaseMiddleware):
#     async def on_pre_process_update(self, update: types.Update, data: dict):
#         user_id = None
#
#         if update.message:
#             user_id = update.message.from_user.id
#             if update.message.text in ["/start", "/help"]:
#                 return
#             user_message = update.message
#         elif update.callback_query:
#             user_id = update.callback_query.from_user.id
#             if update.callback_query.data == "tekshir":
#                 return
#             user_message = update.callback_query.message
#         else:
#             return
#
#         text = "⛔ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:\n\n"
#         is_all_subscribed = True
#
#         # Inline tugmalar
#         markup = types.InlineKeyboardMarkup(row_width=1)
#
#         for channel in CHANNELS:
#             is_subscribed = await obuna.check(user_id=user_id, channel=channel)
#             if not is_subscribed:
#                 is_all_subscribed = False
#                 chat = await bot.get_chat(channel)
#                 invite_link = await chat.export_invite_link()
#                 text += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"
#                 markup.add(types.InlineKeyboardButton(text=chat.title, url=invite_link))
#
#         if not is_all_subscribed:
#             try:
#                 await user_message.delete()  # Foydalanuvchi yuborgan xabarni o‘chirish
#             except:
#                 pass
#
#             # Oxirida "Obuna tekshiruvi" tugmasi
#             markup.add(types.InlineKeyboardButton(text="✅ Obuna tekshiruvi", callback_data="tekshir"))
#
#             await user_message.answer(text, reply_markup=markup, disable_web_page_preview=True)
#             raise CancelHandler()