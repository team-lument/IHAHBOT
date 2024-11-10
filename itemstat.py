import sqlite3, requests
AYAGG_API_KEY = "Bearer 2eae1a86-8593-4b52-b806-0eb5f587a22a"
AYAGG_API_URL = "https://api.aya.gg"
AYAGG_HEADER = { 'Authorization': AYAGG_API_KEY }

# get ayagg data
def get_ayagg_data():
	response = requests.get(AYAGG_API_URL+'/static/items', headers=AYAGG_HEADER)
	data = response.json()
	# connect to sqlite
	conn = sqlite3.connect('ERData/Item.db')
	c = conn.cursor()
	for item in data['result']:
		c.execute("UPDATE Item SET category=?,stack=?,credit=?,initalc=? WHERE id=?", (item['itemSubcategoryId'], item['stackable'], item['vfCredits'], item['initialCount'], item['id']))
		#c.execute(f"INSERT INTO ItemStat(id) VALUES({item['id']})")
		for options in list(item['options'].keys()):
			c.execute(f'UPDATE ItemStat SET {options}=? WHERE id=?', (item['options'][options] if type(item['options'][options]) == int else f"{item['options'][options]}", item['id']))
		conn.commit()
		print(f'{item["id"]} is updated')

def getCategoryFromAyagg():
	response = requests.get(AYAGG_API_URL+'/static/item-subcategories', headers=AYAGG_HEADER)
	data = response.json()
	conn = sqlite3.connect('ERData/Item.db')
	c = conn.cursor()
	for category in data['result']:
		c.execute(f"INSERT INTO Category VALUES(?,?,?,?)", (category['id'],category['categoryId'],category['weaponId'],category['index']))
		conn.commit()
		print(f'{category["id"]} is updated')

getCategoryFromAyagg()