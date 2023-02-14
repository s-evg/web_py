from aiohttp import ClientSession, TCPConnector
import time
import asyncio
from dbapp import create_db, db_insert, db_select


URL = "https://swapi.dev/api/"

pers_info = {
    "films": {},
    "species": {},
    "starships": {},
    "planets": {},
    "vehicles": {}
    }

names = {
    "films": "title",
    "species": "name",
    "starships": "name",
    "planets": "name",
    "vehicles": "name",
    "people": None
    }


async def get_info(sem, session, url, retry=5):
    """Собираем данные о персонажах"""

    try:
        async with session.get(url=url) as response:
            response_json = await response.json()
    except Exception as ex:
        if retry:
            print(f"[INFO] retry={retry} => {url}")
            time.sleep(3)
            return await get_info(sem, session, url, retry=(retry - 1))
        else:
            raise
    else:
        print(f"[INFO] Обработал страницу {url}")
        return response_json


async def semaphore(sem, session, url):
    """Настраиваем количество одновременных запросов от установленного семафора"""
    async with sem:
        return await get_info(sem, session, url)


async def gather_data():
    """Подготавливаем задачи для запросов"""
    tasks = []
    persones = []

    sem = asyncio.Semaphore(20)  # устанавливаем количество одновременных подключений

    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        for page, name in names.items():
            for page_id in range(100):  # генерируем все страницы для сбора названий и имён
                url = f"https://swapi.dev/api/{page}/{page_id}"
                task = asyncio.create_task(semaphore(sem, session, url))
                tasks.append(task)

            __info__ = await asyncio.gather(*tasks)
            tasks.clear()
            if names[page]:
                for info in __info__:
                    url = info.get('url')
                    if url:
                        pers_info[page][url] = info.get(names[page])
            else:
                pers_info["homeworld"] = pers_info["planets"]
                pers_info.pop("planets")
                for pers in __info__:
                    if "detail" not in pers:
                        for pi in pers_info:
                            element = pers.get(pi)
                            if type(element) is str:
                                element = [element]  # в основном для ключа "homeworld"
                            info = [pers_info[pi].get(_) for _ in element]
                            # print(f"{pi} === >>> {element} | {info}")
                            if None not in info:
                                pers[pi] = ", ".join(info)
                            else:
                                pers[pi] = "no"

                        pers["pers_id"] = pers["url"].split("/")[-2]
                        persones.append(pers)
                        data = [
                            pers["pers_id"],
                            pers["birth_year"],
                            pers["eye_color"],
                            pers["films"],
                            pers["gender"],
                            pers["hair_color"],
                            pers["height"],
                            pers["homeworld"],
                            pers["mass"],
                            pers["name"],
                            pers["skin_color"],
                            pers["species"],
                            pers["starships"],
                            pers["vehicles"]
                        ]
                        await db_insert(data)

        return persones


def main():
    asyncio.run(create_db())
    asyncio.run(gather_data())
    return asyncio.run(db_select())


if __name__ == "__main__":
    start = time.time()
    pers = main()
    for per in pers:
        print(per)
    print(f"Выполнено за: {time.time() - start} c")
