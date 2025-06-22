import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMINS = os.getenv("ADMINS")
if ADMINS:
    ADMINS = [int(admin_id.strip()) for admin_id in ADMINS.split(",")]
else:
    ADMINS = []

CHANNELS = [
    "@filmlar_kinolar_multfilmlar",
]
MOVIES_FILE = 'data/movies.json'
CHANNELS_FILE = 'data/channels.json'
USERS_FILE = 'data/users.json'
LOG_FILE = 'data/logs.json'