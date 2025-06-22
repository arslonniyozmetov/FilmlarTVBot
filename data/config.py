import os
import json
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMINS = os.getenv("ADMINS")
if ADMINS:
    ADMINS = [int(admin_id.strip()) for admin_id in ADMINS.split(",")]
else:
    ADMINS = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
MOVIES_FILE = os.path.join(DATA_DIR, "movies.json")
CHANNELS_FILE = os.path.join(DATA_DIR, "channels.json")
LOGS_FILE = os.path.join(DATA_DIR, "logs.json")

# 📡 Kanallarni channels.json dan yuklab olish
CHANNELS = []
if os.path.exists(CHANNELS_FILE):
    try:
        with open(CHANNELS_FILE, "r") as f:
            data = json.load(f)
            for channel in data.get("channels", []):
                CHANNELS.append(channel['link'])
    except Exception as e:
        print("Kanallarni yuklashda xatolik:", e)
