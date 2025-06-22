from aiogram import Bot

async def check_subscription(bot: Bot, user_id: int, channel: str) -> bool:
    try:
        member = await bot.get_chat_member(channel, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False
