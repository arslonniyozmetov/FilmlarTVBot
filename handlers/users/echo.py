from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import CHANNELS, ADMINS
from handlers.users.kino_qidiruv import get_kino_by_id_handler, qidir_kino
from keyboards.inline.kanalar import kanalar_button
from loader import dp, bot, db
from states.kino_qidiruv import KinoQidiruv
from utils.misc import obuna

@dp.message_handler(state=None)
async def bot_echo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    msg_text = message.text  # foydalanuvchi yuborgan kino ID bo'lishi mumkin

    data = await state.get_data()
    if data.get("checked"):
        return  # Avval tekshirgan bo‘lsa, hech narsa qilmaymiz

    all_channels = True
    markup = InlineKeyboardMarkup(row_width=1)

    for index, channel in enumerate(CHANNELS, start=1):
        if not await obuna.check(user_id=user_id, channel=channel):
            all_channels = False
            try:
                chat = await bot.get_chat(channel)
                invite_link = await chat.export_invite_link()
            except:
                invite_link = f"https://t.me/{channel.lstrip('@')}"
            markup.add(InlineKeyboardButton(text=f"{index}-kanal", url=invite_link))

    if all_channels:
        await message.answer("✅ Obuna tekshiruvi muvaffaqiyatli yakunlandi!")
        await state.update_data(checked=True)

        # Agar avval kiritilgan kino raqami mavjud bo‘lsa, uni qayta ishlaymiz
        if msg_text.isdigit():
            await KinoQidiruv.waiting_for_kino_id.set()
            await state.update_data(kino_id_text=msg_text)

            # Kino qidirish funksiyasini chaqiramiz
            await qidir_kino(message, state)

        else:
            await message.answer("🔎 Qaysi kino ID raqamini qidiramiz? Yozing:")
            await KinoQidiruv.waiting_for_kino_id.set()

    else:
        markup.add(InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="tekshir"))
        await state.update_data(temp_msg=msg_text)  # vaqtincha saqlab qo'yamiz
        await message.answer(
            "❗ Quyidagi kanal(lar)ga obuna bo‘ling va qayta tekshiring:",
            reply_markup=markup,
            disable_web_page_preview=True
        )


@dp.callback_query_handler(text="tekshir", state="*")
async def tekshir_obuna(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    all_channels = True

    for channel in CHANNELS:
        if not await obuna.check(user_id=user_id, channel=channel):
            all_channels = False
            break

    if all_channels:
        await call.message.delete()
        await call.message.answer("✅ Obuna tekshiruvi muvaffaqiyatli yakunlandi!")
        await state.update_data(checked=True)

        data = await state.get_data()
        kino_id_text = data.get("temp_msg")

        if kino_id_text and kino_id_text.isdigit():
            await KinoQidiruv.waiting_for_kino_id.set()
            await state.update_data(kino_id_text=kino_id_text)

            # Kino ID yuborilganidek qo‘lda message yasaymiz:
            dummy_msg = types.Message(
                message_id=call.message.message_id,
                from_user=call.from_user,
                chat=call.message.chat,
                date=call.message.date,
                text=kino_id_text,
                bot=call.bot
            )
            await get_kino_by_id_handler(dummy_msg, state)  # bevosita handlerni chaqiramiz
        else:
            await call.message.answer("🔎 Qaysi kino ID raqamini qidiramiz? Yozing:")
            await KinoQidiruv.waiting_for_kino_id.set()
    else:
        await call.answer("❗ Hali ham barcha kanallarga obuna emassiz.", show_alert=True)
#
# @dp.message_handler(state=None)
# async def bot_echo(message: types.Message, state: FSMContext):
#     message = message.text
#     user_id = message.from_user.id
#
#     data = await state.get_data()
#     if data.get("checked"):
#         return  # ❗ Oldin tekshirilgan foydalanuvchi, boshqa ishlamasin
#
#     all_channels = True
#     markup = InlineKeyboardMarkup(row_width=1)
#
#     for index, channel in enumerate(CHANNELS, start=1):
#         if not await obuna.check(user_id=user_id, channel=channel):
#             all_channels = False
#             try:
#                 chat = await bot.get_chat(channel)
#                 invite_link = await chat.export_invite_link()
#             except:
#                 invite_link = f"https://t.me/{channel.lstrip('@')}"
#
#             # Raqamli nom bilan tugma qo‘shish (kanal nomi emas)
#             markup.add(InlineKeyboardButton(text=f"{index}-kanal", url=invite_link))
#
#     if all_channels:
#         await message.answer("✅ Obuna tekshiruvi muvaffaqiyatli yakunlandi!")
#         # await message.answer("Xush kelibsiz!\n🔎 Qaysi kino ID raqamini qidiramiz? Yozing:")
#         await state.update_data(checked=True)
#         await KinoQidiruv.waiting_for_kino_id.set()
#     else:
#         markup.add(InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="tekshir"))
#         await message.answer(
#             "❗ Quyidagi kanal(lar)ga obuna bo‘ling va qayta tekshiring:",
#             reply_markup=markup,
#             disable_web_page_preview=True
#         )
#
#
#
# @dp.callback_query_handler(text="tekshir")
# async def tekshir(call: CallbackQuery, state: FSMContext):
#     await call.answer()
#     user_id = call.from_user.id
#
#     # Kanal manzillari va ularning tartib raqami
#     kanal_info = [
#         ("1-kanal", "https://t.me/FilmsTopChannels?start=FilmsTop01_bot"),
#         ("2-kanal", "https://t.me/Kino_Time121?start=FilmsTop01_bot"),
#     ]
#
#     all_subscribed = True
#     markup = InlineKeyboardMarkup(row_width=1)
#
#     for index, channel in enumerate(CHANNELS):
#         status = await obuna.check(user_id=user_id, channel=channel)
#         if not status:
#             all_subscribed = False
#             kanal_raqam, kanal_link = kanal_info[index]
#             markup.add(InlineKeyboardButton(text=kanal_raqam, url=kanal_link))
#
#     if all_subscribed:
#         await call.message.delete()  # ❗️ eski xabarni o‘chiramiz
#         await call.message.answer("✅ Obuna tekshiruvi muvaffaqiyatli yakunlandi!")
#         # await call.message.answer("Xush kelibsiz!\n🔎 Qaysi kino ID raqamini qidiramiz? Yozing:")
#         await state.update_data(checked=True)
#         await KinoQidiruv.waiting_for_kino_id.set()
#     else:
#         await call.message.delete()  # ❗️ eski xabarni o‘chiramiz
#         markup.add(InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="tekshir"))
#         await call.message.answer(
#             text="❗ Quyidagi kanal(lar)ga obuna bo‘ling va qayta tekshiring:",
#             reply_markup=markup,
#             disable_web_page_preview=True
#         )