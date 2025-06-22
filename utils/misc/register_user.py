import os
import json
from datetime import datetime

USERS_FILE = 'data/users.json'

async def register_user(user):
    os.makedirs("data", exist_ok=True)
    data = {"users": []}

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            data = json.load(f)

    if not any(u['user_id'] == user.id for u in data["users"]):
        user_data = {
            "user_id": user.id,
            "first_name": user.first_name,
            "username": user.username or "",
            "register_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data["users"].append(user_data)

        with open(USERS_FILE, "w") as f:
            json.dump(data, f, indent=4)
