from math import ceil

def getVersion():
	return "BETAv4"

def getSeason(seasonId: int):
	seasonName = round(seasonId/2)
	if seasonId == 0:     return '일반'
	if seasonId % 2 == 0: return f'프리시즌 {seasonName if seasonId <= 16 else seasonName-9}'
	else:                 return f'{'정규' if seasonId >= 17 else 'EA'} 시즌 {seasonName-9 if seasonId >= 17 else seasonName}'

def getTeamType(teamType: int):
	if teamType == 1:   return '솔로'
	elif teamType == 2: return '듀오'
	elif teamType == 3: return '스쿼드'
	elif teamType == 4: return '코발트'

roma = ["", "I", "II", "III", "IV"]

def getTierName(mmr: int, demigod: bool = False, eternity: bool = False):
	if mmr < 600:
		return [f"아이언 {roma[ceil(mmr/150)]}", f"{mmr%150}점", "iron"]
	elif mmr < 1400:
		return [f"브론즈 {roma[ceil((mmr-600)/200)]}", f"{(mmr-600)%200}점", "bronze"]
	elif mmr < 2400:
		return [f"실버 {roma[ceil((mmr-1400)/250)]}", f"{(mmr-1400)%250}점", "silver"]
	elif mmr < 3600:
		return [f"골드 {roma[ceil((mmr-2400)/300)]}", f"{(mmr-2400)%300}점", "gold"]
	elif mmr < 5000:
		return [f"플래티넘 {roma[ceil((mmr-3600)/350)]}", f"{(mmr-3600)%350}점", "platinum"]
	elif mmr < 6400:
		return [f"다이아몬드 {roma[ceil((mmr-5000)/350)]}", f"{(mmr-5000)%350}점", "diamond"]
	elif mmr < 6800:
		return [f"메테오라이트", f"{mmr-6400}점", "meteorite"]
	else:
		return [f"이터니티", f"{mmr-6800}점", "eternity"] if eternity else [f"데미갓", f"{mmr-6800}점", "demigod"] if demigod else [f"미스릴", f"{mmr-6800}점", "mithril"]