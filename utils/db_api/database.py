films = {
    "1": {"title": "Titanik", "description": "Romantik drama", "url": "https://t.me/yourchannel/1"},
    "2": {"title": "Inception", "description": "Fantastik triller", "url": "https://t.me/yourchannel/2"},
    "3": {"title": "Shawshank", "description": "Motivatsion drama", "url": "https://t.me/yourchannel/3"},
}

async def get_film_by_code(code: str):
    return films.get(code)

async def add_film(code: str, title: str, description: str, url: str):
    films[code] = {
        "title": title,
        "description": description,
        "url": url
    }
import aiosqlite

DB_PATH = "path_to_your_sqlite_db.sqlite"  # O'z yo'lingizni qo'ying

async def get_user_count() -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0