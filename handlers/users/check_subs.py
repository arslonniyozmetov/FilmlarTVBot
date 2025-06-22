import logging

from aiogram import Bot
from aiogram.types import ChatMemberStatus


logger = logging.getLogger(__name__)

async def check_subscription(bot: Bot, user_id: int, channel: str) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in [
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER
        ]
    except Exception as e:
        logger.error(f"❗ Error for user {user_id} in channel {channel}: {e}")
        return False
