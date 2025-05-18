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
