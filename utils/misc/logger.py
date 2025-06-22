import json
import os
from datetime import datetime
from data.config import LOGS_FILE

async def log_movie_view(movie_id, user_id):
    os.makedirs(os.path.dirname(LOGS_FILE), exist_ok=True)

    data = {"views": []}
    if os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, "r") as f:
            data = json.load(f)

    log_entry = {
        "movie_id": movie_id,
        "user_id": user_id,
        "viewed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data["views"].append(log_entry)
    with open(LOGS_FILE, "w") as f:
        json.dump(data, f, indent=4)
