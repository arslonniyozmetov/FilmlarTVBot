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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "../data/users.json")
MOVIES_FILE = os.path.join(BASE_DIR, "../data/movies.json")
CHANNELS_FILE = os.path.join(BASE_DIR, "../data/channels.json")
LOGS_FILE = os.path.join(BASE_DIR, "../data/logs.json")