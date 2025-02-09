import sqlite3, aiohttp
from urllib.parse import quote
from config import API_URL, API_HEADER, AYAGG_API_URL, AYAGG_HEADER

async def getRecord(userId: int, page: int=None):
	async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
		async with session.get(AYAGG_API_URL + f"/matches/by-player/{userId}{f'?page={page}' if page else ''}") as res:
			r = await res.json()
			return r

async def getRecord_Match(match: int, userId: int=None):
	async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
		if userId:
			async with session.get(AYAGG_API_URL + f"/participants/by-match/{match}") as res:
				r = await res.json()
				for x in r['result']:
					if x['playerId'] == userId: return x

async def searchUser(query: str=None):
	async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
		async with session.get(AYAGG_API_URL + f"/search/players?nameQuery={quote(query)}") as res:
			r = await res.json()
			return r

async def getUser(*, nick: str=None, userId: int=None):
	if nick:
		return [nick, await getUserId(nick)]
	if userId:
		async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
			async with session.get(AYAGG_API_URL + f"/matches/by-player/{userId}") as res:
				r = await res.json()
				if res.status == 404: return [None, userId]
				return [r['result'][0]['recordedName'], userId]

async def getUserId(nick: str):
	conn = sqlite3.connect("database/player.db")
	c = conn.cursor()
	c.execute(f"SELECT userId FROM player WHERE nickname='{nick}'")
	n = c.fetchone()
	# if n == None:	# TODO: Old Nickname Search
	# 	c.execute(f"SELECT userId FROM player WHERE nicknameOld='{nick}'")
	# 	n = c.fetchone()
	if n == None:
		async with aiohttp.ClientSession(headers=API_HEADER) as session:
			async with session.get(API_URL + f"/v1/user/nickname?query={nick}") as res:
				r = await res.json()
				if r['status'] == 404:
					return None
				c.execute(f"SELECT * FROM player WHERE userId={r['user']['userNum']}")
				if c.fetchone():
					c.execute(f"UPDATE player SET nickname='{nick}' WHERE userId={r['user']['userNum']}")
				else:
					c.execute(f"INSERT INTO player(userId, nickname) VALUES({r['user']['userNum']}, '{nick}')")
				conn.commit()
				return r['user']['userNum']
	return n[0]

def getUserNickname(userId: int):
	conn = sqlite3.connect("database/player.db")
	c = conn.cursor()
	c.execute(f"SELECT nickname FROM player WHERE userId={userId}")
	n = c.fetchone()
	if n == None:
		return None
	return n[0]

async def getUserLevel(userId: int):
	conn = sqlite3.connect("database/player.db")
	c = conn.cursor()
	c.execute(f"SELECT accountLevel FROM player WHERE userId={userId}")
	n = c.fetchone()
	nick = getUserNickname(userId)
	if n == None or n[0] == None:
		async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
			async with session.get(AYAGG_API_URL + f"/player/by-name/{nick}") as res:
				r = await res.json()
				if res.status == 404: return None
				data = r['result']['level']
				c.execute(f"UPDATE player SET accountLevel={data} WHERE userId={userId}")
				conn.commit()
				return data
	return n[0]

async def getUserStatistics(userId: int, season: int=None):
	result = {}
	async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
		async with session.get(AYAGG_API_URL + f"/player/{userId}/statistics") as res:
			r = await res.json()
			result['overall'] = r['overall']
		async with session.get(AYAGG_API_URL + f"/player/{userId}/statistics{f'?seasonId={season}' if season else ''}") as res:
			r = await res.json()
			result['season'] = r['overall']
		async with session.get(AYAGG_API_URL + f"/queues/by-player/{userId}") as res:
			r = await res.json()
			for x in r['result']:
				if x['seasonId'] == season: result['seasonQueueData'] = x
		return result

async def getUserMMRHistory(userId: int, queue: int=3):
	async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
		async with session.get(AYAGG_API_URL + f"/queues/by-player/{userId}/history") as res:
			r = await res.json()
			try:
				return r['result'][f'{queue}']
			except:
				return None