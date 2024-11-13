import sqlite3

def getMemberSetting(userId: int, guildId: int, key: str="locale"):
	conn = sqlite3.connect("database/serviceData.db")
	c = conn.cursor()
	c.execute(f"SELECT {key} FROM guildedUser WHERE userId={userId} AND guildId={guildId}")
	n = c.fetchone()
	if n != None:
		if n[0] == 1 or n[0] == 0:
			if key == "hideNick" or key == "hideGameId":
				return True if n[0] == 1 else False
		return n[0]
	else:
		if key == "locale":
			setMemberSetting(userId, guildId, "locale", "ko")
			return "ko"
		if key == "hideNick":
			setMemberSetting(userId, guildId, "hideNick", "false")
			return False
		if key == "hideGameId":
			setMemberSetting(userId, guildId, "hideGameId", "false")
			return False

def setMemberSetting(userId: int, guildId: int, key: str, value: str):
	conn = sqlite3.connect("database/serviceData.db")
	c = conn.cursor()
	c.execute(f"SELECT * FROM guildedUser WHERE userId={userId} AND guildId={guildId}")
	n = c.fetchone()
	if not n:
		c.execute(f"INSERT INTO guildedUser(userId, guildId) VALUES ({userId}, {guildId})")
	if key == "locale":
		c.execute(f"UPDATE guildedUser SET locale='{value}' WHERE userId={userId} AND guildId={guildId}")
	if key == "hideNick":
		c.execute(f"UPDATE guildedUser SET hideNick={1 if value == 'true' else 0} WHERE userId={userId} AND guildId={guildId}")
	if key == "hideGameId":
		c.execute(f"UPDATE guildedUser SET hideGameId={1 if value == 'true' else 0} WHERE userId={userId} AND guildId={guildId}")
	conn.commit()
	conn.close()

def getUserSetting(userId: int, key: str="locale"):
	conn = sqlite3.connect("database/serviceData.db")
	c = conn.cursor()
	c.execute(f"SELECT {key} FROM user WHERE userId={userId}")
	n = c.fetchone()
	if n != None:
		return n[0]
	else:
		return None

def setUserSetting(userId: int, key: str, value: str):
	conn = sqlite3.connect("database/serviceData.db")
	c = conn.cursor()
	c.execute(f"SELECT * FROM user WHERE userId={userId}")
	n = c.fetchone()
	if not n:
		c.execute(f"INSERT INTO user (userId) VALUES ({userId})")
	if key == "gameNickname":
		c.execute(f"UPDATE user SET gameNickname={value} WHERE userId={userId}")
	conn.commit()
	conn.close()

def getGuildSetting(guildId: int, key: str="locale"):
	conn = sqlite3.connect("database/serviceData.db")
	c = conn.cursor()
	c.execute(f"SELECT {key} FROM guild WHERE guildId={guildId}")
	n = c.fetchone()
	if n != None:
		return n[0]
	else:
		return None

def setGuildSetting(guildId: int, key: str, value: str):
	conn = sqlite3.connect("database/serviceData.db")
	c = conn.cursor()
	c.execute(f"SELECT * FROM guild WHERE guildId={guildId}")
	n = c.fetchone()
	if not n:
		c.execute(f"INSERT INTO guild (guildId) VALUES ({guildId})")
	if key == "locale":
		c.execute(f"UPDATE guild SET locale='{value}' WHERE guildId={guildId}")
	conn.commit()
	conn.close()