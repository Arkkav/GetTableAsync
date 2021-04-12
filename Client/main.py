import aiohttp
import asyncio
import time


async def get_rows(url, session, params):
    async with session.get(url, params=params) as response:
        print(response.status)
        return await response.read()


async def run(rows):
    url = "http://localhost:8000/"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with aiohttp.ClientSession() as session:
        for i in rows:
            task = asyncio.create_task(get_rows(url, session, {'n': str(i)}))
            tasks.append(task)
        return await asyncio.gather(*tasks)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run([1, 10, 100]))
asyncio.run(run([1, 10, 100]))



