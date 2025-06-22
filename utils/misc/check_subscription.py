import os
import json
from loader import bot
from data.config import CHANNELS_FILE

async def check_subscription(user_id, channel_link):
    """
    Har bitta kanal uchun foydalanuvchining obuna bo‘lganligini tekshiradi
    """
    try:
        member = await bot.get_chat_member(chat_id=channel_link, user_id=user_id)
        if member.status in ['left', 'kicked']:
            return False
        return True
    except:
        return False

async def get_channels():
    """
    channels.json dan kanallarni o‘qib olish
    """
    channels = []
    if os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, "r") as f:
            data = json.load(f)
            for channel in data.get("channels", []):
                channels.append(channel['link'])
    return channels
