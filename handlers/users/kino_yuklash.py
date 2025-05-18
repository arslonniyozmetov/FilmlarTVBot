from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters.private_chat import IsPrivate
from loader import dp, db, bot
from data.config import ADMINS, CHANNELS
from states.kino import Post
from filters.admin import AdminFilter
from keyboards.inline.yuborish import yuborish, post_callback
from keyboards.inline.yuklab_olish import korish_button



@dp.message_handler(AdminFilter(), IsPrivate(), Command("kino"))
async def kino(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id

    if str(user_id) in ADMINS:
        await message.answer("Kino text kiriting:")
        await Post.text.set()
    else:
        await message.answer(f"Uzur so'rayman <b>{user_name}</b>, siz kino qo'sha olmaysiz.", parse_mode="HTML")


@dp.message_handler(state=Post.text)
async def nomi_post(message: Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        data["name"] = name
    await Post.kino.set()
    await message.answer("Kino kiriting:")


@dp.message_handler(state=Post.kino, content_types=types.ContentType.VIDEO)
async def tag_post(message: Message, state: FSMContext):
    kino = message.video.file_id
    async with state.proxy() as data:
        data["kino"] = kino
    await Post.ID.set()
    await message.answer("Kino ID kiriting:")


@dp.message_handler(state=Post.ID)
async def davlat_post(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("❗ Iltimos, faqat raqamdan iborat kino ID kiriting.")
        return  # Shu yerda to‘xtaydi, holat o‘zgarmaydi

    ID = message.text
    async with state.proxy() as data:
        data["ID"] = ID

    await message.answer("Kino video kiriting:")
    await Post.video.set()


@dp.message_handler(state=Post.video, content_types=types.ContentType.VIDEO)
async def rasm_post(message: types.Message, state: FSMContext):
    data = await state.get_data()
    video = message.video.file_id
    async with state.proxy() as data:
        data["video"] = video

    await db.add_kino(
        id=int(data["ID"]),
        kino_file_id=data["kino"],
        image_file_id=video  # Passing the video as image_file_id
    )

    msg_text = (
        f"🎬 Kino nomi: {data['name']}\n"
    )
    await message.answer_video(video=video, caption=msg_text, reply_markup=yuborish)
    await state.finish()


@dp.callback_query_handler(post_callback.filter(action="yuborish"), user_id=ADMINS)
async def confirm_post(call: types.CallbackQuery):
    await call.answer("✅ Chop etishga ruhsat berdingiz.", show_alert=True)
    await call.message.edit_reply_markup()

    try:
        # Sending video instead of photo
        await bot.send_video(
            chat_id=CHANNELS[1],
            video=call.message.video.file_id,  # Sending video file
            caption=call.message.caption,  # Adding caption
            reply_markup=korish_button  # Attach the buttons
        )
    except Exception as e:
        await call.message.answer(f"❌ Kanalga yuborishda xatolik: {e}")


@dp.callback_query_handler(post_callback.filter(action="to'xtatish"), user_id=ADMINS)
async def cancel_post_admin(call: types.CallbackQuery):
    await call.answer("❌ Post bekor qilindi.", show_alert=True)
    await call.message.edit_reply_markup()