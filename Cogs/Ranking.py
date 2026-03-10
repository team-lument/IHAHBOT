from math import floor
import disnake
from disnake.ext import commands
from Cogs.Stat import RecordListView
from module.database import getAllCharacterName, getCharacterName, searchCharacter
from module.embed import makeErrorEmbed
from module.games import getRecordOptions
from module.player import getRecord
from module.ranking import getRanking_Artisan, getRanking_LP, getRanking_LP_Server
from module.variables import getTierName

class PreviousPage(disnake.ui.Button['RankingView']):
	def __init__(self, userId: int, page: int, length: int, artisan: bool, server: int = 0):
		self._userId = userId
		self._page = page
		self._length = length
		self._artisan = artisan
		self._server = server
		super().__init__(emoji="◀️", style=disnake.ButtonStyle.blurple, disabled=page <= 0)
	
	async def callback(self, i: disnake.Interaction):
		if self._userId == i.user.id:
			await i.response.defer()
			if self._server != 0:
				ranking = (await getRanking_LP_Server(self._server))['topRanks'][(self._page-1)*25:self._page*25+1]
				rankList = makeRanking_LP(ranking)
			else:
				ranking = await getRanking_LP(floor((self._page-1)/2))
				rankList = makeRanking(ranking['result'], back=True if int((self._page-1)/2) != (self._page-1)/2 else False, artisan=self._artisan)
			await i.edit_original_message(view=RankingView(self._userId, self._page-1, self._length, rankList, artisan=self._artisan, server=self._server))
		else:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)

class NextPage(disnake.ui.Button['RankingView']):
	def __init__(self, userId: int, page: int, length: int, artisan: bool, server: int = 0):
		self._userId = userId
		self._page = page
		self._length = length
		self._artisan = artisan
		self._server = server
		super().__init__(emoji="▶️", style=disnake.ButtonStyle.blurple, disabled=True if page == length-1 else False)
	
	async def callback(self, i: disnake.Interaction):
		if self._userId == i.user.id:
			await i.response.defer()
			if self._server != 0:
				ranking = (await getRanking_LP_Server(self._server))['topRanks'][(self._page+1)*25:(self._page+2)*25+1]
				rankList = makeRanking_LP(ranking)
			else:
				ranking = await getRanking_LP(floor((self._page+1)/2))
				rankList = makeRanking(ranking['result'], back=True if int((self._page+1)/2) != (self._page+1)/2 else False, artisan=self._artisan)
			await i.edit_original_message(view=RankingView(self._userId, self._page+1, self._length, rankList, artisan=self._artisan, server=self._server))
		else:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)

class ChangePageModal(disnake.ui.Modal):
	def __init__(self, userId: int, page: int, length: int, artisan: bool, server: int = 0):
		self._length = length
		self._userId = userId
		self._artisan = artisan
		self._server = server
		components = [
			disnake.ui.TextInput(
				label="페이지",
				placeholder=f"{page+1} ~ {length-1}까지 입력하세요.",
				value=f"{page+1}",
				custom_id="page_goto",
				required=True,
				style=disnake.TextInputStyle.short,
				max_length=len(str(length))
			)
		]
		
		super().__init__(title="페이지 이동", components=components, custom_id="ChangePageModal")
	
	async def callback(self, i: disnake.ModalInteraction):
		self._page = int(i.text_values['page_goto'])-1
		if self._page > self._length: await i.response.send_message(embed=makeErrorEmbed("최대 페이지를 초과할 수 없어요!"), ephemeral=True)
		if self._server != 0:
			ranking = (await getRanking_LP_Server(self._server))['topRanks'][self._page*25:(self._page+1)*25+1]
			rankList = makeRanking_LP(ranking)
		else:
			ranking = await getRanking_LP(floor((self._page)/2))
			rankList = makeRanking(ranking['result'], back=True if int((self._page)/2) != (self._page)/2 else False, artisan=self._artisan)
		await i.response.edit_message(view=RankingView(self._userId, self._page, self._length, rankList, artisan=self._artisan, server=self._server))

class ChangePage(disnake.ui.Button):
	def __init__(self, userId: int, page: int, length: int, artisan: bool, server: int = 0):
		self._userId = userId
		self._page = page
		self._length = length
		self._artisan = artisan
		self._server = server
		super().__init__(label=f"{page+1} / {length-1}", style=disnake.ButtonStyle.gray)
	
	async def callback(self, i: disnake.Interaction):
		if self._userId == i.user.id:
			await i.response.send_modal(ChangePageModal(self._userId, self._page, self._length, self._artisan, self._server))
		else:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)

class RankList(disnake.ui.Select):
	def __init__(self, userId: int, rankList: list[disnake.SelectOption]):
		self._userId = userId
		super().__init__(placeholder="RP 랭킹", options=rankList)

	async def callback(self, i: disnake.MessageInteraction):
		if self._userId == i.user.id:
			await i.response.defer(with_message=True)
			userId = int(self.values[0])
			record = await getRecord(userId)
			nick = record['result'][0]['recordedName']
			embed = disnake.Embed(
				title=f"{nick}님의 전적",
				description="원하는 기록을 선택하고 전적을 확인해보세요!"
			).set_footer(text="이하봇 • 팀 루멘트가 ♥️로 제작")
			await i.edit_original_message(embed=embed, view=RecordListView(i.user.id, await getRecordOptions(record['result'], i), userId, record['page'], nick))
		else:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)

class RankingView(disnake.ui.View):
	def __init__(self, userId: int, page: int, length: int, rankList: list[disnake.SelectOption], *, artisan: bool = False, server: int = 0):
		super().__init__(timeout=None)
		self.add_item(PreviousPage(userId, page, length, artisan, server))
		self.add_item(ChangePage(userId, page, length, artisan, server))
		self.add_item(NextPage(userId, page, length, artisan, server))
		self.add_item(RankList(userId, rankList))

class Ranking(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.slash_command(
		name=disnake.Localized(
			"ranking",
			data={
				disnake.Locale.ko: "랭킹"
			}
		),
		description=disnake.Localized(
			"Ranking commands.",
			data={
				disnake.Locale.ko: "랭킹 명령어의 모음입니다."
			}
		)
	)
	async def ranking_slashCommand(self, i: disnake.CommandInteraction):
		pass

	@ranking_slashCommand.sub_command(
		name="rp",
		description=disnake.Localized(
			"Get RP ranking for now season",
			data={
				disnake.Locale.ko: "프리 시즌이 아닌 현재 시즌의 RP 랭킹을 불러옵니다."
			}
		),
		options=[
			disnake.Option(
				name="server",
				description=disnake.Localized(
					"Server ID",
					data={
						disnake.Locale.ko: "서버 ID"
					}
				),
				type=disnake.OptionType.integer,
				required=False,
				choices=[
					disnake.OptionChoice(name=disnake.Localized(
						"Asia",
						data={
							disnake.Locale.ko: "아시아"
						}
					), value=10),
					disnake.OptionChoice(name=disnake.Localized(
						"Asia2",
						data={
							disnake.Locale.ko: "아시아2"
						}
					), value=17),
					disnake.OptionChoice(name=disnake.Localized(
						"NorthAmerica",
						data={
							disnake.Locale.ko: "북미"
						}
					), value=12),
					disnake.OptionChoice(name=disnake.Localized(
						"Europe",
						data={
							disnake.Locale.ko: "유럽"
						}
					), value=13),
					disnake.OptionChoice(name=disnake.Localized(
						"SouthAmerica",
						data={
							disnake.Locale.ko: "남미"
						}
					), value=14)
				]
			)
		]
	)
	async def ranking_rp_cmd(
		self, i: disnake.CommandInteraction,
		server: int = 10
	):
		await i.response.defer()
		serverList = {
			10 : "아시아",
			17 : "아시아2",
			12 : "북미",
			13 : "유럽",
			14 : "남미"
		}
		ranking = (await getRanking_LP_Server(server))['topRanks']
		rankList = makeRanking_LP(ranking)
		highRank = {
			"eternity": { "mmr": ranking[299]['mmr'], "rank": 300 },
			"demigod": { "mmr": ranking[999]['mmr'], "rank": 1000 }
		}
		for x in range(1,301 if len(ranking) >= 300 else len(ranking)):
			if ranking[x]['mmr'] < 7900 and ranking[x]['rank'] <= 300:
				highRank['eternity']['mmr'] = ranking[x-1]['mmr']
				highRank['eternity']['rank'] = ranking[x-1]['rank']
				break
		if len(ranking) > 300:
			for x in range(300,len(ranking)):
				if ranking[x]['mmr'] < 7900 and ranking[x]['rank'] <= 1000:
					highRank['demigod']['mmr'] = 7900
					highRank['demigod']['rank'] = ranking[x]['rank']
					break
		embed = disnake.Embed(
			title=f"{serverList[server]} RP 랭킹",
			description=f"이터니티 컷: {highRank['eternity']['mmr']}점 ({highRank['eternity']['rank']}위)\n-# 7900점 이상, 300위 이내\n\n데미갓 컷: {highRank['demigod']['mmr']}점 ({highRank['demigod']['rank']}위)\n-# 7900점 이상, 1000위 이내"
		).set_footer(text="이하봇 • 팀 루멘트가 ♥️로 제작")
		await i.edit_original_message(embed=embed, view=RankingView(i.user.id, 0, 40, rankList, server=server))#(ranking['page'][1]-1)*2, rankList))
	
	async def artisan_autocomplete(i: disnake.CommandInteraction, character: str):
		listFrom = searchCharacter(character)
		if listFrom == None: listFrom = await getAllCharacterName()
		listRes = []
		for x in listFrom:
			if len(listRes) < 25: listRes.append(disnake.OptionChoice(name=x[1] if i.locale is disnake.Locale.ko else x[2], value=x[0]))
		return listRes

	# aya.gg terminated 😭
	
	# @ranking_slashCommand.sub_command(
	# 	name=disnake.Localized(
	# 		"artisan",
	# 		data={
	# 			disnake.Locale.ko: "장인력"
	# 		}
	# 	),
	# 	description=disnake.Localized(
	# 		"Get artisan ranking for now season",
	# 		data={
	# 			disnake.Locale.ko: "프리 시즌이 아닌 현재 시즌의 장인력 랭킹을 불러옵니다."
	# 		}
	# 	)
	# )
	# async def ranking_artisan_cmd(
	# 	self, i: disnake.CommandInteraction,
	# 	character: int = commands.Param(
	# 		name=disnake.Localized(
	# 			"character",
	# 			data={
	# 				disnake.Locale.ko: "실험체"
	# 			}
	# 		),
	# 		description=disnake.Localized(
	# 			"Character Name.",
	# 			data={
	# 				disnake.Locale.ko: "실험체 이름"
	# 			}
	# 		),
	# 		autocomplete=artisan_autocomplete
	# 	)
	# ):
	# 	await i.response.defer()
	# 	ranking = await getRanking_Artisan(characterId=character)
	# 	rankList = makeRanking(ranking['result'], artisan=True)
	# 	embed = disnake.Embed(
	# 		title=f"{getCharacterName(character)} 장인력 랭킹"
	# 	).set_footer(text="이하봇 • 팀 루멘트가 ♥️로 제작")
	# 	await i.edit_original_message(embed=embed, view=RankingView(i.user.id, 0, (ranking['page'][1]-1)*2, rankList, True))

def makeRanking(r: dict, back: bool = False, artisan: bool = False):
	rankList = []
	for tmp in range(51):
		if (back and tmp >= 25 and len(rankList) < 25) or (not back and len(rankList) < 25):
			x = r[tmp]; rank = x['index']+1
			if tmp > 0 and x['value'] == r[tmp-1]['value']: rank -= 1
			rankList.append(disnake.SelectOption(label=f"#{rank} {x['playerName']}", description=f"{' '.join(getTierName(x['value'], x['queueTable']['3']['isDemigod'], x['queueTable']['3']['isEternity'])[0:1])} ({x['value']}LP)" if not artisan else f"{x['value']}점", value=x['playerId']))
	return rankList

def makeRanking_LP(r: dict):
	rankList = []
	for tmp in range(25):
		if len(rankList) < 25:
			x = r[tmp]; rank = x['rank']
			if tmp > 0 and x['mmr'] == r[tmp-1]['mmr']: rank -= 1
			rankList.append(disnake.SelectOption(label=f"#{rank} {x['nickname']}", description=f"{' '.join(getTierName(x['mmr'], x['mmr'] >= 7900 and x['rank'] <= 300, x['mmr'] >= 7900 and x['rank'] <= 1000)[0:1])} ({x['mmr']}LP)", value=x['nickname']))
	return rankList

def setup(bot: commands.Bot):
	bot.add_cog(Ranking(bot))