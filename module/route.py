import aiohttp
from config import *
from module.database import getSkill

async def getRoute(*, id: int=0, name: str=""):
	async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
		if name:
			async with session.get(AYAGG_API_URL + f'/search/routes?titleQuery={name}') as req:
				r = await req.json()
			return r
		if not id: return None
		async with session.get(AYAGG_API_URL + f'/route/{id}?cache=no') as req:
			r = await req.json()
		return r

def generateSkillTree(r: list):
	tree = []; master = {}
	for x in r: tree.append(getSkill(x, "slot")[0])
	for x in ["Q", "W", "E", "R", "T"]: n = len(tree) - 1 - tree[::-1].index(x); master[x] = n; tree[n] = f"**{tree[n]}**"
	master.pop("T", None)
	return [tree, list(dict(sorted(master.items(), key=lambda item: item[1])).keys())]