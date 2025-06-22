import json
from data.config import MOVIES_FILE

async def get_film_by_code(code: str):
    if not code.isdigit():
        return None
    code = int(code)
    try:
        with open(MOVIES_FILE, "r") as f:
            movies = json.load(f).get("movies", [])
        for movie in movies:
            if movie["id"] == code:
                return movie
    except:
        pass
    return None
