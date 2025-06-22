import os
import json

MOVIES_FILE = 'data/movies.json'

async def get_film_by_code(code):
    if not os.path.exists(MOVIES_FILE):
        return None

    with open(MOVIES_FILE, "r") as f:
        data = json.load(f)

    for movie in data.get("movies", []):
        if str(movie['id']) == str(code):
            return {
                "title": movie['name'],
                "genre": movie['genre'],
                "country": movie['country'],
                "language": movie['language'],
                "quality": movie['quality'],
                "year": movie['year'],
                "duration": movie['duration'],
                "rating": movie['rating'],
                "file_id": movie['file_id']
            }
    return None
