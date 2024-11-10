import aiohttp
from config import AYAGG_API_URL, AYAGG_HEADER

async def getRanking_LP(page: int=0):
	async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
		async with session.get(AYAGG_API_URL + f"/ranking/mmr/by-queue/3?page={page}") as res:
			return await res.json()

async def getRanking_Artisan(characterId: int, page: int=0):
	async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
		async with session.get(AYAGG_API_URL + f"/ranking/artisan/{characterId}?page={page}") as res:
			return await res.json()