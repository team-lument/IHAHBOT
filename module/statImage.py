import os, sqlite3, logging
from PIL import Image, ImageDraw, ImageFont
from module.variables import getTierName, getSeason
from module.database import *
import urllib.request
import plotly.express as px
from pandas import DataFrame
from datetime import datetime
from dateutil.relativedelta import relativedelta

logger = logging.getLogger("ihahbot.main")

def getRankCode(itemCode: int):
	conn = sqlite3.connect('ERData/Item.db', isolation_level=None)
	c = conn.cursor()
	c.execute(f"SELECT rank FROM Item WHERE id={itemCode}")
	rank = c.fetchone()
	if rank and rank[0]:
		return int(rank[0])
	else:
		return 0

class Point(object):
	def __init__(self, x, y):
		self.x, self.y = x, y

class Rect(object):
	def __init__(self, x1, y1, x2, y2):
		minx, maxx = (x1,x2) if x1 < x2 else (x2,x1)
		miny, maxy = (y1,y2) if y1 < y2 else (y2,y1)
		self.min = Point(minx, miny)
		self.max = Point(maxx, maxy)

	width  = property(lambda self: self.max.x - self.min.x)
	height = property(lambda self: self.max.y - self.min.y)


def gradient_color(minval, maxval, val, color_palette):
	""" Computes intermediate RGB color of a value in the range of minval
		to maxval (inclusive) based on a color_palette representing the range.
	"""
	max_index = len(color_palette)-1
	delta = maxval - minval
	if delta == 0:
		delta = 1
	v = float(val-minval) / delta * max_index
	i1, i2 = int(v), min(int(v)+1, max_index)
	(r1, g1, b1), (r2, g2, b2) = color_palette[i1], color_palette[i2]
	f = v - i1
	return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

def horz_gradient(draw, rect, color_func, color_palette):
	minval, maxval = 1, len(color_palette)
	delta = maxval - minval
	width = float(rect.width)  # Cache.
	for x in range(rect.min.x, rect.max.x+1):
		f = (x - rect.min.x) / width
		val = minval + f * delta
		color = color_func(minval, maxval, val, color_palette)
		draw.line([(x, rect.min.y), (x, rect.max.y)], fill=color)

def vert_gradient(draw, rect, color_func, color_palette):
	minval, maxval = 1, len(color_palette)
	delta = maxval - minval
	height = float(rect.height)  # Cache.
	for y in range(rect.min.y, rect.max.y+1):
		f = (y - rect.min.y) / height
		val = minval + f * delta
		color = color_func(minval, maxval, val, color_palette)
		draw.line([(rect.min.x, y), (rect.max.x, y)], fill=color)

def getX(size, bgColor, message, font):
    W, H = size
    image = Image.new('RGB', size, bgColor)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    return (W-w)/2

def generateRecordImage(x: dict, disable: dict = {"nickname": 0, "gameId": 0}):
	try:
		# First Background
		image = Image.open("image/Background/Background.png")
		draw = ImageDraw.Draw(image)
		print("Background1 Loaded")

		# Skin
		_characterId = x['characterId'] if x['characterId'] >= 10 else f"0{x['characterId']}"
		_characterSkinIndex = x['characterSkinIndex'] if x['characterSkinIndex'] >= 10 else f"0{x['characterSkinIndex']}"
		skin = Image.open(f"image/skinFull/{getSkinUrl_String(int(f'10{_characterId}0{_characterSkinIndex}'))}.png").resize((1400, 1400))
		image.paste(skin, (-300, 0), skin)
		print("Character Skin Loaded")

		# Second Background
		bg2 = Image.open("image/Background/BG_Right.png")
		image.paste(bg2, (0, 0), bg2)
		print("Background2 Loaded")

		# ID
		font = ImageFont.truetype('Freesentation-7Bold.ttf', size=48)
		if disable['gameId'] == 0:
			draw.text((22, 18), f"#{x['matchId']}", font=font, fill="#838383")
		print("Match ID Loaded")

		# Nickname
		font = ImageFont.truetype('Freesentation-7Bold.ttf', size=80)
		if disable['nickname'] == 0:
			draw.text((835, 105), f"{x['recordedName']}", font=font, fill="white")
		else:
			draw.text((835, 105), f"닉네임 비공개", font=font, fill="#A7A7A7")
		print("Nickname Loaded")

		# Game Type
		seasonId = x['seasonId']
		mtm = int(x['queueType'])

		if mtm == 4:
			GameType = Image.open("image/Background/CobaltGame.png")
			image.paste(GameType, (1024, 336), GameType)
		if mtm <= 3 and seasonId == 0:
			GameType = Image.open("image/Background/NormalGame.png")
			image.paste(GameType, (1024, 336), GameType)
		elif mtm <= 3 and seasonId > 0:
			GameType = Image.open("image/Background/RankedGame.png")
			image.paste(GameType, (1024, 336), GameType)
		
		if mtm == 3:
			GameType = Image.open("image/Background/TeamSquad.png")
			image.paste(GameType, (1476, 336), GameType)
		elif mtm == 2:
			GameType = Image.open("image/Background/TeamDuo.png")
			image.paste(GameType, (1476, 336), GameType)
		elif mtm == 1:
			GameType = Image.open("image/Background/TeamSolo.png")
			image.paste(GameType, (1476, 336), GameType)
		print("Game Type Loaded")

		# Game Rank
		if x['activityFlags']['escapeState'] == 3:
			im = Image.open("image/Flags/submarine.png")
			image.paste(im, (853, 327))
		else:
			font = ImageFont.truetype('Inter-Bold.ttf', size=100)
			draw.text((855, 330), f"#{x['rank']}", font=font, fill="#FFFFFF" if x['rank'] > 3 else "#207ac7" if x['rank'] != 1 else "#11b288")
		print("Game Rank Loaded")

		# Flags
		im = Image.open("image/Flags/alpha.png").resize((128, 128))
		if not x['activityFlags']['killedAlpha']:
			im = im.convert("L")
		image.paste(im, (910, 615), im)
		im = Image.open("image/Flags/omega.png").resize((128, 128))
		if not x['activityFlags']['killedOmega']:
			im = im.convert("L")
		image.paste(im, (1056, 615), im)
		im = Image.open("image/Flags/wickline.png").resize((128, 128))
		if not x['activityFlags']['killedWickline']:
			im = im.convert("L")
		image.paste(im, (1202, 615), im)
		print("Flags Loaded")
		
		# KDA
		font = ImageFont.truetype('Inter-Bold.ttf', size=80)
		if x['kill'] >= 10: draw.text((916, 516), f"{x['kill']}", font=font, fill="#000000")
		else: draw.text((944, 516), f"{x['kill']}", font=font, fill="#000000")
		if x['death'] >= 10: draw.text((1068, 516), f"{x['death']}", font=font, fill="#000000")
		else: draw.text((1096, 516), f"{x['death']}", font=font, fill="#000000")
		if x['assist'] >= 10: draw.text((1220, 516), f"{x['assist']}", font=font, fill="#000000")
		else: draw.text((1248, 516), f"{x['assist']}", font=font, fill="#000000")
		print("KDA Loaded")
		
		# Damage
		font = ImageFont.truetype('Inter-Bold.ttf', size=80)
		draw.text((1382+((5-len(str(x['totalDeal'])))*26), 516), f"{x['totalDeal']}", font=font, fill="#000000")
		print("Damage Loaded")

		# RP
		font = ImageFont.truetype('Inter-Bold.ttf', size=80)
		rpAdder = (3-len(str(x['afterMMR']-x['recordedMMR'])))*26
		if mtm <= 3 and seasonId > 0:
			if x['afterMMR']-x['recordedMMR'] >= 0:
				draw.text((1664+rpAdder, 516), f"+", font=font, fill="#039C00")
				draw.text((1718+rpAdder, 516), f"{x['afterMMR']-x['recordedMMR']}", font=font, fill="#000000")
			else:
				draw.text((1664+rpAdder, 516), f"-", font=font, fill="#FF1414")
				draw.text((1718+rpAdder, 516), f"{abs(x['afterMMR']-x['recordedMMR'])}", font=font, fill="#000000")
		else:
			draw.text((1750, 516), f"-", font=font, fill="#000000")
		
		# Character Level
		font = ImageFont.truetype('Inter-Bold.ttf', size=80)
		if x['level'] >= 10:
			draw.text((852, 214), f"{x['level']}", font=font, fill="#FFFFFF")
		else:
			draw.text((872, 214), f"{x['level']}", font=font, fill="#FFFFFF")
		print("Character Level Loaded")
		
		# Weapon
		_weaponId = x['itemSubcategoryIndex']
		font = ImageFont.truetype('Inter-Bold.ttf', size=80)
		image.paste(Image.open(f"image/Weapons/{WeaponName(_weaponId)}.png").resize((94, 90)), (1004, 214), Image.open(f"image/Weapons/{WeaponName(_weaponId)}.png").resize((94, 90)))
		draw.text((1108, 210), f"{x['preferences']['masteries'][f'{_weaponId}']}", font=font, fill="#FFFFFF")
		print("Weapon Loaded")
		
		# Trait
		trait = x['preferences']['traits']
		print("firstCore", trait['firstCore'])
		if os.path.isfile(f"image/Trait/{trait['firstCore']}.png"):
			im = Image.open(f"image/Trait/{trait['firstCore']}.png").resize((128, 128))
			image.paste(im, (892, 842), im)
		else:
			im = Image.open(f"image/Trait/none.png").resize((128, 128))
			image.paste(im, (892, 842), im)
			logger.error(f"statImage.makeImage | firstCore {trait['firstCore']} Image not Found")
		coord = [(1038, 842), (1184, 842)]
		for tmp in range(len(trait['firstSub'])):
			print(f"firstSub{tmp}", trait['firstSub'][tmp])
			if os.path.isfile(f"image/Trait/{trait['firstSub'][tmp]}.png"):
				im = Image.open(f"image/Trait/{trait['firstSub'][tmp]}.png").resize((128, 128))
				image.paste(im, coord[tmp], im)
			else:
				im = Image.open(f"image/Trait/none.png").resize((128, 128))
				image.paste(im, coord[tmp], im)
				logger.error(f"statImage.makeImage | firstSub{tmp} {trait['firstSub'][tmp]} Image not Found")
		print("Trait(Main) Loaded")
		coord = [(1330, 842), (1476, 842)]
		for tmp in range(len(trait['secondSub'])):
			print(f"secondSub{tmp}", trait['secondSub'][tmp])
			if os.path.isfile(f"image/Trait/{trait['secondSub'][tmp]}.png"):
				im = Image.open(f"image/Trait/{trait['secondSub'][tmp]}.png").resize((128, 128))
				image.paste(im, coord[tmp], im)
			else:
				im = Image.open(f"image/Trait/none.png").resize((128, 128))
				image.paste(im, coord[tmp], im)
				logger.error(f"statImage.makeImage | secondSub{tmp} {trait['secondSub'][tmp]} Image not Found")
		print("Trait(Sub) Loaded")

		# Tactical Skill
		if x['spellId']:
			im = Image.open(f"image/TacticalSkills/{x['spellId']}.png").resize((128,128))
			image.paste(im, (1728, 842), im)
			font = ImageFont.truetype('Inter-Bold.ttf', size=80)
			draw.text((1822, 908), f"{x['spellLevel']}", font=font, fill="#F9FD3B")
		print("Tactical Skill Loaded")

		# Items
		RECT = [
			Rect(866, 1087, 1066, 1213), Rect(1073, 1087, 1273, 1213), Rect(1281, 1087, 1481, 1213),
			Rect(1489, 1087, 1689, 1213), Rect(1697, 1087, 1897, 1213)
		]
		EQUIP = [
			(869, 1097), (1081, 1097), (1287, 1097),
			(1494, 1097), (1703, 1097)
		]
		repler = [
			[[(64, 64, 64), (128, 128, 128)], "common"],
			[[(7, 51, 0), (14, 102, 0)], "uncommon"],
			[[(39, 45, 58), (51, 74, 107)], "rare"],
			[[(54, 43, 64), (102, 71, 133)], "epic"],
			[[(72, 58, 35), (194, 150, 41)], "legendary"],
			[[(61, 31, 33), (144, 49, 49)], "mythic"]
		]
		equip = x['preferences']['equipments']
		_matchVersion = int(x['matchVersion'][2:4])
		for i in range(5):
			print(i, equip[i])
			_slot = getItemSlot(int(equip[i]))
			vert_gradient(draw, RECT[_slot], gradient_color, repler[getRankCode(int(equip[i]))][0])
			if not os.path.isfile(f"image/Items/{equip[i]}.png"):
				saveItemImage(int(equip[i]), _matchVersion)
			try:
				characterEquipment = Image.open(f"image/Items/{equip[i]}.png").convert("RGBA")
			except Exception as e:
				backup = getItemBackup(int(equip[i]))
				if backup:
					if not os.path.isfile(f"image/Items/{backup}.png"):
						saveItemImage(int(backup), _matchVersion)
					characterEquipment = Image.open(f"image/Items/{backup}.png").convert("RGBA")
				else:
					saveItemImage(int(equip[i]), _matchVersion)
					characterEquipment = Image.open(f"image/Items/{equip[i]}.png").convert("RGBA")
			characterEquipment = characterEquipment.resize((192, 106))
			image.paste(characterEquipment, EQUIP[_slot], characterEquipment)
		bg2 = Image.open("image/Background/BG_Item.png")
		image.paste(bg2, (830, 1048), bg2)
		print("Items Loaded")

		# Save
		image.save(f"Match/{x['playerId']}.png")
		logger.debug(f"statImage.makeImage | {x['playerId']} # {x['matchId']}")
	except Exception as e:
		logger.error(f"statImage.makeImage | {e}")
		return e

def getTier(mmr: int, demigod: bool = False, eternity: bool = False):
	if eternity:		return "eternity"
	elif demigod: 		return "demigod"
	elif mmr == 0: 		return "unranked"
	elif mmr < 600: 	return "iron"
	elif mmr < 1400: 	return "bronze"
	elif mmr < 2400: 	return "silver"
	elif mmr < 3600: 	return "gold"
	elif mmr < 5000: 	return "platinum"
	elif mmr < 6400: 	return "diamond"
	elif mmr < 6800: 	return "meteorite"
	else:				return "mithril"

rankTierColors = {
	"unranked": 	"rgb(240, 240, 240)",
	"iron": 		"rgb(229, 239, 255)",
	"bronze": 		"rgb(252, 149, 59)",
	"silver": 		"rgb(96, 127, 161)",
	"gold": 		"rgb(224, 184, 102)",
	"platinum": 	"rgb(122, 225, 175)",
	"diamond": 		"rgb(208, 196, 226)",
	"metheorite": 	"rgb(105, 159, 229)",
	"mithril": 		"rgb(130, 208, 225)",
	"demigod": 		"rgb(255, 255, 222)",
	"eternity": 	"rgb(160, 31, 74)"
}

def generateMMRHistoryImage(userId: int, data: dict, tier: str):
	keys = list(data); day = datetime.today() + relativedelta(days=-15); df = []; tierColors = []; tierColors = []; opacity = []; dataIndex = None
	while dataIndex == None:
		if day.strftime("%y%m%d") in keys: dataIndex = day.strftime("%y%m%d")
		day += relativedelta(days=-1)
	day = datetime.today() + relativedelta(days=-16)
	for _ in range(17):
		if day.strftime("%y%m%d") in keys: dataIndex = day.strftime("%y%m%d")
		if (
			day.strftime("%y%m%d") != datetime.today().strftime("%y%m%d")
	  	) and not (
			(day + relativedelta(days=1)).strftime("%y%m%d") in keys
		):
			opacity.append(0)
			tierColors.append("rgba(0, 0, 0, 0)")
		else:
			opacity.append(1)
			tierColors.append(rankTierColors[tier])
		df.append({ "date": day.strftime("%m/%d"), "rp": data[dataIndex]['end']})
		day += relativedelta(days=1)
	frame = DataFrame.from_dict(df)
	fig = px.line(frame, x="date", y="rp", text="rp")
	fig.update_traces(
		textposition="top center",
		textfont=dict(
			color=tierColors
		),
		line=dict(
			color='white',
			width=5
		),
		marker=dict(
			color=tierColors,
			colorscale='Viridis',
			cmin=0,
			cmax=50,
			size=15,
			opacity=opacity
		)
	)

	fig.update_xaxes(title=None, dtick=2)
	fig.update_yaxes(title=None, dtick=100)
	fig.update_layout(
		margin=dict(
			autoexpand=False,
			l=50,
			r=20,
			t=20,
			b=30
		),
		plot_bgcolor='rgba(0, 0, 0, 0)',
		paper_bgcolor='rgba(0, 0, 0, 0)',
		xaxis=dict(
			gridcolor='#575757',
			color='white',
			tickfont=dict(
				color='white'
			)
		),
		yaxis=dict(
			gridcolor='#575757',
			color='white',
			tickfont=dict(
				color='white'
			)
		)
	)
	fig.write_image(f"Match/mmr-history/{userId}.png")

def generateStatImage(user: list, x: dict, history: dict):
	image = Image.open("image/Background/Tier/_Background.png")
	draw = ImageDraw.Draw(image)
	
	userId = user[0]; userName = user[1]; tier = getTierName(x['seasonQueueData']['mmr'], x['seasonQueueData']['isDemigod'], x['seasonQueueData']['isEternity'])

	draw.text((75, 25), f"{userName}", font=ImageFont.truetype('Freesentation-7Bold.ttf', size=40), fill="#FFFFFF")
	draw.text((30, 75), f"{x['overall']['plays']}전 {x['overall']['wins']}승 ({round((x['overall']['wins']/x['overall']['plays'])*100, 1)}%)", font=ImageFont.truetype('Freesentation-7Bold.ttf', size=20), fill="#959595")

	tierBackground = Image.open(f"image/Background/Tier/{tier[2].capitalize()}.png")
	image.paste(tierBackground, (25, 112), tierBackground)

	statusTitle  = ImageFont.truetype('Freesentation-7Bold.ttf', size=13)
	statusObject = ImageFont.truetype('Freesentation-7Bold.ttf', size=16)

	draw.text((125, 135), f"{getSeason(x['seasonQueueData']['seasonId'])}", font=ImageFont.truetype('Freesentation-7Bold.ttf', size=18), fill=(206, 206, 206))
	draw.text((125, 160), f"{tier[0]}", font=ImageFont.truetype('Freesentation-7Bold.ttf', size=27), fill="#FFFFFF")
	draw.text((123, 190), f"{x['seasonQueueData']['mmr']}", font=ImageFont.truetype('Inter-Bold.ttf', size=40), fill=rankTierColors[tier[2]])
	draw.text((255+(-30*(5-len(f"{x['seasonQueueData']['mmr']}")))+(5 if len(f"{x['seasonQueueData']['mmr']}") >= 4 else 10), 200), "RP", font=ImageFont.truetype('Inter-Bold.ttf', size=30), fill="#FFFFFF")
	draw.text((412, 408), "GENERATED BY IHAHBOT", font=ImageFont.truetype('Inter-Bold.ttf', size=15), fill="#959595")

	draw.text(( 45, 270), "평균 K·D·A", font=statusTitle, fill="#E0E0E0")
	draw.text((165, 270), "승률", font=statusTitle, fill="#E0E0E0")
	draw.text((230, 270), "반타작률", font=statusTitle, fill="#E0E0E0")
	draw.text(( 45, 340), "게임 수", font=statusTitle, fill="#E0E0E0")
	draw.text((135, 340), "승리 수", font=statusTitle, fill="#E0E0E0")
	draw.text((230, 340), "플레이 시간", font=statusTitle, fill="#E0E0E0")
	draw.text((315, 155), "RP 변동 이력", font=statusTitle, fill="#E0E0E0")

	draw.text(( 45, 285), f"{round(x['season']['kda'][0]/x['seasonQueueData']['totalPlays'], 1)} · {round(x['season']['kda'][1]/x['seasonQueueData']['totalPlays'], 1)} · {round(x['season']['kda'][2]/x['seasonQueueData']['totalPlays'], 1)}", font=statusObject, fill="#FFFFFF")
	draw.text((165, 285), f"{round((x['seasonQueueData']['totalWins']/x['seasonQueueData']['totalPlays'])*100, 1)}%", font=statusObject, fill="#FFFFFF")
	draw.text((230, 285), f"{round(x['season']['halfRate']*100, 1)}%", font=statusObject, fill="#FFFFFF")
	draw.text(( 45, 355), f"{x['seasonQueueData']['totalPlays']}", font=statusObject, fill="#FFFFFF")
	draw.text((135, 355), f"{x['seasonQueueData']['totalWins']}", font=statusObject, fill="#FFFFFF")
	draw.text((230, 355), f"{round(x['season']['playTime']/3600, 1)}시간", font=statusObject, fill="#FFFFFF")

	foreground = Image.new("RGBA", (image.width, image.height), (0, 0, 0, 0))
	tierSmallBackground = Image.open(f"image/Tier/Small/{tier[2].capitalize()}.png").convert("RGBA")
	foreground.paste(tierSmallBackground, (25, 30), tierSmallBackground)
	image = Image.alpha_composite(image, foreground)

	image = image.resize((image.width*3, image.height*3))
	foreground = Image.new("RGBA", (image.width, image.height), (0, 0, 0, 0))
	tierFullImage = Image.open(f"image/Tier/Full/{tier[2].capitalize()}.png").resize((240,375)).convert("RGBA")
	foreground.paste(tierFullImage, (130, 425 if x['seasonQueueData']['mmr'] < 1400 else 370), tierFullImage)
	image = Image.alpha_composite(image, foreground)

	generateMMRHistoryImage(userId, history, tier[2])
	RPHistory = Image.open(f"Match/mmr-history/{userId}.png").resize((800, 600)).convert("RGBA")
	foreground = Image.new("RGBA", (image.width, image.height), (0, 0, 0, 0))
	foreground.paste(RPHistory, (930, 525), RPHistory)
	image = Image.alpha_composite(image, foreground)

	image.save(f"Match/Stat/{userId}.png")

def getItemSlot(itemId: int):
	conn = sqlite3.connect('ERData/Item.db')
	c = conn.cursor()
	c.execute(f"SELECT category FROM Item WHERE id=?", (itemId,))
	n = c.fetchone()
	c.execute(f"SELECT imageSlot FROM Category WHERE sub=?", (n[0],))
	n = c.fetchone()
	return n[0]

def saveItemImage(itemId: int, version: int):
	try:
		urllib.request.urlretrieve(f"https://cdn.dak.gg/assets/er/game-assets/1.{version}.0/ItemIcon_{itemId}.png", "image/Items/temp.png")
		bg = Image.open("image/Items/save.png")
		item = Image.open(f"image/Items/temp.png")
		bg.paste(item, (int((bg.width - item.width)/2), 0), item)
		bg.save(f"image/Items/{itemId}.png")
		return
	except Exception as e:
		logger.error(f"statImage.saveItemImage | {e}")