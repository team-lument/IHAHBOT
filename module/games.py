import disnake
from disnake.ext import commands
from datetime import datetime
from module.database import getCharacterName, getCustomEmojiId
from module.setting import getMemberSetting
from module.variables import getSeason, getTeamType

async def getRecordOptions(r: dict, i: disnake.CommandInteraction, thisMatch: bool = False):
	options = [ ]
	_i = 0
	for x in r:
		_i += 1
		mtm = int(x['queueType'])
		seasonNum = x['seasonId']
		season = f"{getSeason(seasonNum)} {getTeamType(mtm)}" if mtm != 4 else "코발트 프로토콜"
		character = getCharacterName(x['characterId'], getMemberSetting(i.user.id, i.guild.id, "locale"))
		assistant = x['assist'] if mtm != 1 else "-"
		rank = int(x['rank'])
		if mtm == 4: rank = "승리" if rank == 1 else "패배"
		valueId = x['matchId'] if not thisMatch else x['playerId']
		if type(rank) == int:
			emoji=disnake.PartialEmoji(
				name=f"rank{rank}",
				id=getCustomEmojiId(f'rank{rank}')
			)
		else:
			if rank == "승리":
				emoji = disnake.PartialEmoji(
					name=f"rank_win",
					id=getCustomEmojiId('rank_win')
				)
			else:
				emoji = disnake.PartialEmoji(
					name=f"rank_lose",
					id=getCustomEmojiId('rank_lose')
				)
		if x['activityFlags']['escapeState'] == 3:
			rank = "탈출"
			emoji = disnake.PartialEmoji(
						name="submarine",
						id=1015205983213076531
					)
		if thisMatch:
			options.append(
				disnake.SelectOption(
					label=f"#{rank} {x['recordedName']}",
					description=f"{x['kill']}/{x['death']}/{assistant} │ {character}",
					value=f"rec.{_i}.{valueId}",
					emoji=emoji
				)
			)
		else:
			endDate = datetime.fromtimestamp(x['matchFinishedAt']/1000).strftime("%m/%d %H:%M")
			options.append(
				disnake.SelectOption(
					label=f"#{rank} {character} | {x['kill']}/{x['death']}/{assistant}",
					description=f"{season} | {endDate}",
					value=f"rec.{_i}.{valueId}",
					emoji=emoji
				)
			)
	return options

"""
import pymongo, aiohttp
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
#from config import MongoDB_URL, API_URL, HEADER

API_URL = "https://api.aya.gg"
HEADER = { "Authorization": "Bearer 2eae1a86-8593-4b52-b806-0eb5f587a22a" }

client = MongoClient("mongodb+srv://ihah:Zkflsgkxm1@coren.sdyvyuh.mongodb.net/", server_api=ServerApi('1'))
db = client.ihahbot

async def getMatchData(userNum: int, gameId: int):
	data = db.match.find_one({"userNum":userNum, "gameId":gameId})
	if data: return data
	else:
		async with aiohttp.ClientSession(headers=HEADER) as session:
			async with session.get(API_URL + f"/v1/user/games/{userNum}?next={gameId + 1}") as res:
				r = await res.json()
				if r['code'] == 200:
					return r['userGames'][0]

async def getMatchList(userNum: int, limit: int = 10):
	for x in db.match.find({"userNum":userNum}).sort("gameId", pymongo.DESCENDING).skip(1).limit(limit):
		print(x)
		# async with aiohttp.ClientSession(headers=HEADER) as session:
		# 	async with session.get(API_URL + f"/v1/user/games/{userNum}?next=0") as res:
		# 		data = await res.json()
		# 		if data['code'] == 200:
		# 			return data['data']
		# 		else:
		# 			return None
"""