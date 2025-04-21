import aiohttp
from config import *
from module.variables import nowSeason

async def getRanking_LP(page: int=0):
	async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
		async with session.get(AYAGG_API_URL + f"/ranking/mmr/by-queue/3?page={page}") as res:
			return await res.json()

async def getRanking_LP_Server(server: int=10):
	async with aiohttp.ClientSession(headers=API_HEADER) as session:
		async with session.get(API_URL + f"/v1/rank/top/{await nowSeason()}/3/{server}") as res:
			return await res.json()

async def getRanking_Artisan(characterId: int, page: int=0):
	async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
		async with session.get(AYAGG_API_URL + f"/ranking/artisan/{characterId}?page={page}") as res:
			return await res.json()