from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        # Postgres ulanishni yaratish
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )
        # Kino jadvalini yaratish
        await self.create_table_kino()
        await self.create_table_users()

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False,
                      ):
        # So'rovni bajarish
        async with self.pool.acquire() as connection:
            connection: Connection
            if fetch:
                result = await connection.fetch(command, *args)
            elif fetchval:
                result = await connection.fetchval(command, *args)
            elif fetchrow:
                result = await connection.fetchrow(command, *args)
            elif execute:
                result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        # Foydalanuvchilar jadvalini yaratish
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
            telegram_id BIGINT PRIMARY KEY,
            full_name TEXT NOT NULL,
            username TEXT,
            email TEXT,
            language TEXT DEFAULT 'uz'
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_kino(self):
        # Kino jadvalini yaratish
        sql = """
          CREATE TABLE IF NOT EXISTS kino (
              id SERIAL PRIMARY KEY,
              kino_file_id TEXT NOT NULL,
              image_file_id TEXT NOT NULL
          );
          """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # Parametrlar bilan so'rovni formatlash
        values = []
        for i, key in enumerate(parameters, start=1):
            sql += f"{key} = ${i} AND "
            values.append(parameters[key])
        sql = sql.rstrip(" AND ")
        return sql, tuple(values)

    async def add_kino(self, id, kino_file_id, image_file_id=None):
        sql = """
        INSERT INTO Kino (id, kino_file_id, image_file_id)
        VALUES ($1, $2, $3)
        """
        return await self.execute(sql, id, kino_file_id, image_file_id, execute=True)

    async def add_user(self, full_name, username, telegram_id):
        # Foydalanuvchi qo'shish
        sql = """
        INSERT INTO Users(full_name, username, telegram_id) VALUES($1, $2, $3)
        """
        return await self.execute(sql, full_name, username, telegram_id, execute=True)

    async def select_all_users(self):
        # Barcha foydalanuvchilarni olish
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        # Foydalanuvchi tanlash
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        # Foydalanuvchilar sonini hisoblash
        sql = "SELECT COUNT(*) FROM Users;"
        return await self.execute(sql, fetchval=True)

    async def update_user_email(self, email, telegram_id):
        # Foydalanuvchi emailni yangilash
        sql = """
        UPDATE Users SET email = $1 WHERE telegram_id = $2
        """
        return await self.execute(sql, email, telegram_id, execute=True)

    async def delete_users(self):
        # Foydalanuvchilarni o'chirish
        sql = "DELETE FROM Users"
        return await self.execute(sql, execute=True)

    async def drop_users(self):
        # Foydalanuvchilar jadvalini o'chirish
        sql = "DROP TABLE IF EXISTS Users"
        return await self.execute(sql, execute=True)

    async def get_kino_by_id(self, kino_id):
        sql = """SELECT kino_file_id FROM kino WHERE id = $1"""
        return await self.pool.fetchrow(sql, kino_id)  # asyncpg uchun

    # Kino jadvalini chiqarish
    async def get_all_kino(self):
        sql = "SELECT * FROM kino"
        return await self.execute(sql, fetch=True)


# Yordamchi logger funksiyasi
def logger(statement):
    print(f"""
------------------------------------------
Executing:
{statement}
------------------------------------------
""")