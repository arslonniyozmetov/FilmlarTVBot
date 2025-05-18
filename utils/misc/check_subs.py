from aiogram import Bot
from aiogram.types import ChatMember
import logging

logger = logging.getLogger(__name__)

async def check_subscription(bot: Bot, user_id: int, channel: str) -> bool:
    try:
        member: ChatMember = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except Exception as e:
        logger.error(f"❗ Unexpected error for user {user_id} in channel {channel}: {e}")
        return False
