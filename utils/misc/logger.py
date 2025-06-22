import os
import json
from datetime import datetime

LOG_FILE = 'data/logs.json'

async def log_movie_view(movie_id, user_id):
    os.makedirs("data", exist_ok=True)

    data = {"views": []}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)

    data["views"].append({
        "movie_id": movie_id,
        "user_id": user_id,
        "date": datetime.now().strftime("%Y-%m-%d")
    })

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)
