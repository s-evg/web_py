import asyncio
import time
from pprint import pprint

import aiosqlite


async def create_db():
    """Создаёт БД"""

    async with aiosqlite.connect("base_swapi.db") as connect:
        await connect.execute("""
                CREATE TABLE IF NOT EXISTS "persones"(
                "id" INTEGER,
                "pers_id" TEXT DEFAULT Null,
                "birth_year" TEXT DEFAULT Null,
                "eye_color" TEXT DEFAULT Null,
                "films" TEXT DEFAULT Null,
                "gender" TEXT DEFAULT Null,
                "hair_color" TEXT DEFAULT Null,
                "height" TEXT DEFAULT Null,
                "homeworld" TEXT DEFAULT Null,
                "mass" TEXT DEFAULT Null,
                "name" TEXT DEFAULT Null,
                "skin_color" TEXT DEFAULT Null,
                "species" TEXT DEFAULT Null,
                "starships" TEXT DEFAULT Null,
                "vehicles" TEXT DEFAULT Null,
                PRIMARY KEY("id" AUTOINCREMENT)
                );
                """)
        await connect.commit()


async def db_insert(data):
    """Вставка в базу"""
    async with aiosqlite.connect("base_swapi.db") as connect:
        await connect.execute("""
                INSERT INTO "persones" ("pers_id", "birth_year", "eye_color", "films", "gender", "hair_color",
                "height", "homeworld", "mass", "name", "skin_color", "species", "starships", "vehicles")
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", data)
        await connect.commit()


async def db_select():
    async with aiosqlite.connect("base_swapi.db") as connect:
        async with connect.execute("SELECT * FROM persones") as data:

            return await data.fetchall()


def main():
    asyncio.run(create_db())
    return asyncio.run(db_select())


if __name__ == "__main__":
    start = time.time()
    data = main()
    for d in data:
        print(d)
    print(f"Выполнено за: {time.time() - start} c")