from math import floor
import disnake
from disnake.ext import commands
from Cogs.Stat import RecordListView
from module.database import getAllCharacterName, getCharacterName, searchCharacter
from module.embed import makeErrorEmbed
from module.games import getRecordOptions
from module.player import getRecord
from module.ranking import getRanking_Artisan, getRanking_LP
from module.variables import getTierName

class PreviousPage(disnake.ui.Button['RankingView']):
	def __init__(self, userId: int, page: int, length: int, artisan: bool):
		self._userId = userId
		self._page = page
		self._length = length
		self._artisan = artisan
		super().__init__(emoji="◀️", style=disnake.ButtonStyle.blurple, disabled=page <= 0)
	
	async def callback(self, i: disnake.Interaction):
		if self._userId == i.user.id:
			await i.response.defer()
			ranking = await getRanking_LP(floor((self._page-1)/2))
			rankList = makeRanking(ranking['result'], back=True if int((self._page-1)/2) != (self._page-1)/2 else False, artisan=self._artisan)
			await i.edit_original_message(view=RankingView(self._userId, self._page-1, self._length, rankList, self._artisan))
		else:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)

class NextPage(disnake.ui.Button['RankingView']):
	def __init__(self, userId: int, page: int, length: int, artisan: bool):
		self._userId = userId
		self._page = page
		self._length = length
		self._artisan = artisan
		super().__init__(emoji="▶️", style=disnake.ButtonStyle.blurple, disabled=True if page == length-1 else False)
	
	async def callback(self, i: disnake.Interaction):
		if self._userId == i.user.id:
			await i.response.defer()
			ranking = await getRanking_LP(floor((self._page+1)/2))
			rankList = makeRanking(ranking['result'], back=True if int((self._page+1)/2) != (self._page+1)/2 else False, artisan=self._artisan)
			await i.edit_original_message(view=RankingView(self._userId, self._page+1, self._length, rankList, self._artisan))
		else:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)

class ChangePageModal(disnake.ui.Modal):
	def __init__(self, userId: int, page: int, length: int, artisan: bool):
		self._length = length
		self._userId = userId
		self._artisan = artisan
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
		ranking = await getRanking_LP(floor((self._page)/2))
		rankList = makeRanking(ranking['result'], back=True if int((self._page)/2) != (self._page)/2 else False, artisan=self._artisan)
		await i.response.edit_message(view=RankingView(self._userId, self._page, self._length, rankList, self._artisan))

class ChangePage(disnake.ui.Button):
	def __init__(self, userId: int, page: int, length: int, artisan: bool):
		self._userId = userId
		self._page = page
		self._length = length
		self._artisan = artisan
		super().__init__(label=f"{page+1} / {length-1}", style=disnake.ButtonStyle.gray)
	
	async def callback(self, i: disnake.Interaction):
		if self._userId == i.user.id:
			await i.response.send_modal(ChangePageModal(self._userId, self._page, self._length, self._artisan))
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
			)
			embed.set_footer(text="Data from aya.gg")
			await i.edit_original_message(embed=embed, view=RecordListView(i.user.id, await getRecordOptions(record['result'], i), userId, record['page'], nick))
		else:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)

class RankingView(disnake.ui.View):
	def __init__(self, userId: int, page: int, length: int, rankList: list[disnake.SelectOption], artisan: bool = False):
		super().__init__(timeout=None)
		self.add_item(PreviousPage(userId, page, length, artisan))
		self.add_item(ChangePage(userId, page, length, artisan))
		self.add_item(NextPage(userId, page, length, artisan))
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
		)
	)
	async def ranking_rp_cmd(self, i: disnake.CommandInteraction):
		await i.response.defer()
		ranking = await getRanking_LP()
		topMMR = ranking['topMMR']
		rankList = makeRanking(ranking['result'])
		embed = disnake.Embed(
			title="RP 랭킹",
			description=f"이터컷: {topMMR['top200']}점\n데미컷: {topMMR['top700']}점"
		)
		await i.edit_original_message(embed=embed, view=RankingView(i.user.id, 0, (ranking['page'][1]-1)*2, rankList))
	
	async def artisan_autocomplete(i: disnake.CommandInteraction, character: str):
		listFrom = searchCharacter(character)
		if listFrom == None: listFrom = await getAllCharacterName()
		listRes = []
		for x in listFrom:
			if len(listRes) < 25: listRes.append(disnake.OptionChoice(name=x[1] if i.locale is disnake.Locale.ko else x[2], value=x[0]))
		return listRes

	@ranking_slashCommand.sub_command(
		name=disnake.Localized(
			"artisan",
			data={
				disnake.Locale.ko: "장인력"
			}
		),
		description=disnake.Localized(
			"Get artisan ranking for now season",
			data={
				disnake.Locale.ko: "프리 시즌이 아닌 현재 시즌의 장인력 랭킹을 불러옵니다."
			}
		)
	)
	async def ranking_artisan_cmd(
		self, i: disnake.CommandInteraction,
		character: int = commands.Param(
			name=disnake.Localized(
				"character",
				data={
					disnake.Locale.ko: "실험체"
				}
			),
			description=disnake.Localized(
				"Character Name.",
				data={
					disnake.Locale.ko: "실험체 이름"
				}
			),
			autocomplete=artisan_autocomplete
		)
	):
		await i.response.defer()
		ranking = await getRanking_Artisan(characterId=character)
		rankList = makeRanking(ranking['result'], artisan=True)
		embed = disnake.Embed(
			title=f"{getCharacterName(character)} 장인력 랭킹"
		)
		await i.edit_original_message(embed=embed, view=RankingView(i.user.id, 0, (ranking['page'][1]-1)*2, rankList, True))

def makeRanking(r: dict, back: bool = False, artisan: bool = False):
	rankList = []
	for tmp in range(51):
		if (back and tmp >= 25 and len(rankList) < 25) or (not back and len(rankList) < 25):
			x = r[tmp]; rank = x['index']+1
			if tmp > 0 and x['value'] == r[tmp-1]['value']: rank -= 1
			rankList.append(disnake.SelectOption(label=f"#{rank} {x['playerName']}", description=f"{' '.join(getTierName(x['value'], x['queueTable']['3']['isDemigod'], x['queueTable']['3']['isEternity'])[0:1])} ({x['value']}LP)" if not artisan else f"{x['value']}점", value=x['playerId']))
	return rankList

def setup(bot: commands.Bot):
	bot.add_cog(Ranking(bot))