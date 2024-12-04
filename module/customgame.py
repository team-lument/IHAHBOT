import sqlite3

def createCustomGame(userId: int, guildId: int, name: str, gameType: int=3, open: bool=False, open_user: bool=False, channelId: int=None):
	conn = sqlite3.connect("database/customGame.db"); c = conn.cursor()
	c.execute("INSERT INTO games (name, guild, leader, gameType, open, user_open, channel) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, guildId, userId, gameType, 1 if open else 0, 1 if open_user else 0, channelId))
	conn.commit()
	c.execute("SELECT id FROM games WHERE leader=? AND name=? ORDER BY id DESC", (userId, name))
	n = c.fetchone()
	conn.close()
	return n[0]

def searchCustomGame(*, userId: int=None, name: str=None, end: bool=False):
	conn = sqlite3.connect("database/customGame.db"); c = conn.cursor()
	if userId:
		c.execute("SELECT * FROM games WHERE leader=? AND end=?", (userId, 1 if end else 0))
	else:
		c.execute("SELECT * FROM games WHERE name=? AND end=?", (name, 1 if end else 0))
	return c.fetchall()

def searchAllOpenCustomGame():
	conn = sqlite3.connect("database/customGame.db"); c = conn.cursor()
	c.execute("SELECT * FROM games WHERE open=1 AND end=0")
	return c.fetchall()

def deleteCustomGame(roomId: int):
	conn = sqlite3.connect("database/customGame.db"); c = conn.cursor()
	try:
		conn.execute("BEGIN TRANSACTION;")
		c.execute("""
		INSERT INTO games_archive (id, name, leader, gameType, open, start, end)
		SELECT id, name, leader, gameType, open, start, end FROM games WHERE id = ?;
		""", (roomId,))
		c.execute("DELETE FROM games WHERE id = ?", (roomId,))
		conn.commit()
	except Exception as e:
		conn.rollback()

def joinCustomGame(roomId: int, userId: int, discordId: int):
	try:
		conn = sqlite3.connect("database/customGame.db"); c = conn.cursor()
		c.execute("INSERT INTO users(gameId, discord, ingame) VALUES (?, ?, ?)", (roomId, discordId, userId))
		conn.commit()
	except:
		return False