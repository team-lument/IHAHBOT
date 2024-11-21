import sqlite3, disnake

# Area

def getArea(id: int, locale: str="ko"):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	c.execute(f'SELECT {locale} FROM Area WHERE id=?', (id,))
	n = c.fetchone()
	if n[0] != 'None':
		return n[0]
	else:
		return f'area.{id}'

# Skill

def getSkill(id: int, column: str="*"):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	c.execute(f'SELECT {column} FROM Skills WHERE id=?', (id,))
	a = c.fetchone()
	if a[0] != 'None':
		return a
	else:
		return f'skill.{id}'

# Weapons

def WeaponTxtKo(id):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	c.execute('SELECT ko FROM Category WHERE weaponIndex=?', (id,))
	a = c.fetchone()
	if a[0] != 'None':
		return a[0]
	else:
		return f'weapon.{id}'

def WeaponName(id):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	c.execute('SELECT sub FROM Category WHERE weaponIndex=?', (id,))
	a = c.fetchone()
	if a[0] != 'None':
		return f"{a[0]}"
	else:
		return f'weapon.{id}'

def WeaponEmoji(id):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	c.execute('SELECT sub,emojiId FROM Category WHERE weaponIndex=?', (id,))
	a = c.fetchone()
	if a[0] != 'None':
		return f"<:{a[0]}:{a[1]}>"
	else:
		return f'weapon.{id}'

# Emojis

def getCustomEmojiId(rank: str):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	c.execute(f"SELECT id FROM CustomEmoji WHERE name=?", (rank,))
	n = c.fetchone()
	return n[0]

# Items

def getRankCode(itemCode: int):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	c.execute(f"SELECT rank FROM Item WHERE id={itemCode}")
	rank = c.fetchone()
	rankCode = rank[0]
	return int(rankCode)

async def getItemName(itemCode: int):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	c.execute(f"SELECT ko FROM Item WHERE id={itemCode}")
	name = c.fetchone()[0]
	return name

async def getItemLink(itemCode: int):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	c.execute(f"SELECT en FROM Item WHERE id={itemCode}")
	name = c.fetchone()[0]
	return str(name).replace(" ", "_").replace("'", "_")

def getItemBackup(itemCode: int):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	c.execute(f"SELECT back FROM Item WHERE id={itemCode}")
	n = c.fetchone()
	print(itemCode, n)
	return n[0]

async def getAllCharacterSkins(characterId: int):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	if characterId < 10:
		characterId = f"0{characterId}"
	else:
		characterId = str(characterId)
	c.execute(f"SELECT id,skinName FROM skinData WHERE id like '%0{characterId}0%'")
	n = c.fetchall()
	if n == None or n[0][0] == None:
		return None
	return n[1:]

# Characters

def getCharacterWeapon(cwId: int):
	conn = sqlite3.connect("ERData/Item.db"); c = conn.cursor()
	c.execute(f"SELECT character,weapon FROM CharacterWeapon WHERE id={cwId}")
	return c.fetchone()

def searchCharacter(name: str):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f'SELECT * FROM character WHERE ko LIKE ? OR en LIKE ?', (f"%{name}%", f"%{name}%"))
	return c.fetchall()

async def makeSkinList(characterId: int):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	characterId = f"0{characterId}" if int(characterId) < 10 else str(characterId)
	c.execute(f"SELECT id,skinName,grade FROM skinData WHERE id LIKE '%0{characterId}0%'")
	n = c.fetchall()
	options = []
	repler = ["⬜", "🟩", "🟦", "🟪"]
	for x in range(len(n)):
		if n[x][2] > 0:
			options.append(disnake.SelectOption(label=n[x][1], value=f"{characterId}@{n[x][0]}", emoji=repler[n[x][2]-1]))
	return options

async def getAllCharacterName(locale: str="ko"):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f'SELECT id,{locale} FROM character')
	return c.fetchall()

async def searchCharacterName(name: str, locale: str="ko"):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f'SELECT id,{locale} FROM character WHERE {locale} LIKE "%{name}%"')
	return c.fetchall()

def getCharacterName(id: int=999, locale: str="ko"):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f'SELECT {locale} FROM character WHERE id=?', (id,))
	n = c.fetchone()
	if n is None or n[0] is None:
		return f"character.{id}"
	return n[0]

async def getCharacterPrice(characterId: int):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f"SELECT np,acoin FROM character WHERE id={characterId}")
	return c.fetchone()

async def getCharacterFullImage(characterId: int):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f"SELECT en FROM character WHERE id={characterId}")
	return f"https://aya.gg/media/images/characters/full/{c.fetchone()[0]}_0.png"

async def getCharacterFullName(characterId: int):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f"SELECT ko_full FROM character WHERE id={characterId}")
	return c.fetchone()[0]

async def getCharacterStory(characterId: int):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f"SELECT storyTitle,story FROM character WHERE id={characterId}")
	return c.fetchone()

# Skins

def skinData(id, sender : int):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute('SELECT * FROM skinData WHERE id=?', (id,))
	a = c.fetchone()
	if a[0] != 'None':
		return a[sender]
	else:
		return f'skin.{id}'

async def getSkinVariable(skinId: int, varId: int=0):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f"SELECT var{varId} FROM skinData WHERE id={skinId}")
	return c.fetchone()[0]

async def getSkinName(skinId: int):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f"SELECT skinName FROM skinData WHERE id={skinId}")
	return c.fetchone()[0]

async def getSkinType(skinId: int):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f"SELECT purchaseType FROM skinData WHERE id={skinId}")
	return c.fetchone()[0]

def getSkinUrl_String(skinId: int):
	conn = sqlite3.connect("ERData/Character.db"); c = conn.cursor()
	c.execute(f"SELECT skinUrl FROM skinData WHERE id={skinId}")
	return f"{c.fetchone()[0]}"