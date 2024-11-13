import disnake, aiohttp
from disnake.ext import commands
from config import AYAGG_API_URL, AYAGG_HEADER
from module.embed import makeErrorEmbed
from module.player import getRecord, getRecord_Match, getUserId, getUserMMRHistory, getUserStatistics, searchUser
from module.setting import getMemberSetting
from module.statImage import generateRecordImage, generateStatImage
from module.games import getRecordOptions

class Stat(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.slash_command(
		name=disnake.Localized(
			"stat",
			data={
				disnake.Locale.ko: "전적"
			}
		),
		description=disnake.Localized(
			"Show Eternal Return user stats.",
			data={
				disnake.Locale.ko: "이터널 리턴 유저 전적을 보여줘요. (초성 검색 가능)"
			}
		),
		options=[
			disnake.Option(
				name=disnake.Localized(
					"user",
					data={
						disnake.Locale.ko: "유저명"
					}
				),
				description=disnake.Localized(
					"Eternal Return user nickname.",
					data={
						disnake.Locale.ko: "이터널 리턴 유저명 또는 초성으로 검색"
					}
				),
				type=disnake.OptionType.string,
				required=True
			),
			disnake.Option(
				name=disnake.Localized(
					"hide",
					data={
						disnake.Locale.ko: "메시지_숨기기"
					}
				),
				description=disnake.Localized(
					"See message only for me. (ephemeral message)",
					data={
						disnake.Locale.ko: "메시지 나만 보기 여부"
					}
				),
				type=disnake.OptionType.boolean,
				required=False
			)
		]
	)
	async def userStat(
		self, i: disnake.CommandInteraction,
		user: str, hide: bool = False
	):
		nick = user.replace("⭐", "").replace("🛠️", "").replace("📹", "")
		userId = await getUserId(nick)
		await i.response.defer(ephemeral=hide)
		if not userId:
			userNames = await searchUser(nick); lists = []
			if len(userNames['result']) != 1:
				for x in userNames['result']:
					lists.append(disnake.SelectOption(
						label=x['name']
					))
				embed = disnake.Embed(
					title="검색 결과",
					description="일치하는 유저명이 없어 검색을 시도했어요!\n아래 검색 결과 중에서 원하는 유저를 선택해주세요!"
				)
				await i.edit_original_message(embed=embed, view=userSearchView(lists, i.user.id))
				return
			else:
				nick = userNames['result'][0]['name']
				userId = userNames['result'][0]['id']
		generateStatImage([userId, nick], await getUserStatistics(userId, 27), await getUserMMRHistory(userId))
		record = await getRecord(userId)
		await i.edit_original_message(embed=None, file=disnake.File(fp=f"Match/Stat/{userId}.png", filename=f"Stat-{userId}.png"), view=RecordListView(i.user.id, await getRecordOptions(record['result'], i), userId, record['page']))

class userSearchView(disnake.ui.View):
	def __init__(self, options: list[disnake.SelectOption], userId: int):
		super().__init__()
		self.add_item(userSearch(options, userId))
	
class userSearch(disnake.ui.Select):
	def __init__(self, options: list[disnake.SelectOption], userId: int):
		super().__init__(
			placeholder="검색 결과",
			options=options
		)
		self._userId = userId
	
	async def callback(self, i: disnake.Interaction):
		if self._userId == i.user.id:
			nick = self.values[0]
			userId = await getUserId(nick)
			generateStatImage([userId, nick], await getUserStatistics(userId, 27), await getUserMMRHistory(userId))
			record = await getRecord(userId)
			await i.response.edit_message(embed=None, file=disnake.File(fp=f"Match/Stat/{userId}.png", filename=f"Stat-{userId}.png"), view=RecordListView(i.user.id, await getRecordOptions(record['result'], i), userId, record['page']))
		else:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)

class RecordList(disnake.ui.Select):
	def __init__(self, discordId: int, userId: int, options: list[disnake.SelectOption]):
		super().__init__(
			placeholder="기록을 선택해주세요.",
			options=options,
			custom_id="record_list"
		)
		self._userId = userId
		self._discordId = discordId
	
	async def callback(self, i: disnake.Interaction):
		if self._discordId == i.user.id:
			await i.response.defer()
			embed = disnake.Embed(
				title=f"전적 데이터 획득 중..."
			)
			embed.set_footer(text="Data from aya.gg")
			embed.description = "데이터 획득 중..."
			await i.edit_original_message(embed=embed, attachments=None)
			match = await getRecord_Match(int(self.values[0].split('.')[2]), self._userId)
			embed = disnake.Embed(
				title=f"{match['recordedName']}님의 전적"
			)
			embed.description = "이미지 제작 중..."
			await i.edit_original_message(embed=embed)
			error = generateRecordImage(match, disable={"nickname": getMemberSetting(i.user.id, i.guild.id, "hideNick"), "gameId": getMemberSetting(i.user.id, i.guild.id, "hideGameId")})
			if error:
				await i.edit_original_message(embed=makeErrorEmbed(f"이미지 생성에 실패했어요.\n이 경우 DB에 등록되지 않은 파일이 있는 경우가 대다수에요.\n아래 에러 내용을 [스타라이트 스튜디오](https://discord.gg/cf3D2HCzEh)로 전달해주세요!\n```{error}```"))
				return
			await i.edit_original_message(embed=None,file=disnake.File(fp=f"Match/{self._userId}.png", filename=f"Match-{self._userId}.png"))
		else:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)

class RecordListButton_Previous(disnake.ui.Button):
	def __init__(self, discordId: int, userId: int, page: list[int]):
		super().__init__(
			style=disnake.ButtonStyle.blurple,
			emoji="◀️",
			disabled=True if page[0] == 0 else False,
		)
		self._userId = userId
		self._page = page[0]+1
		self._discordId = discordId
	
	async def callback(self, i: disnake.Interaction):
		if self._discordId != i.user.id:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)
			return
		record = await getRecord(self._userId, self._page-1)
		await i.response.edit_message(view=RecordListView(i.user.id, await getRecordOptions(record['result'], i), self._userId, record['page']))


class ChangePageModal(disnake.ui.Modal):
	def __init__(self, userId: int, page: int, length: int):
		self._userId = userId
		self._length = length
		components = [
			disnake.ui.TextInput(
				label="페이지",
				placeholder=f"{page+1} ~ {length+1}까지 입력하세요.",
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
		record = await getRecord(self._userId, self._page)
		await i.response.edit_message(view=RecordListView(i.user.id, await getRecordOptions(record['result'], i), self._userId, [self._page, self._length]))

class RecordListButton_NowPage(disnake.ui.Button):
	def __init__(self, discordId: int, userId: int, page: list[int]):
		self._discordId = discordId
		self._userId = userId
		self._page = page
		super().__init__(
			style=disnake.ButtonStyle.gray,
			label=f"{page[0]+1} / {page[1]}"
		)
	
	async def callback(self, i: disnake.Interaction):
		if self._discordId != i.user.id:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)
			return
		await i.response.send_modal(ChangePageModal(self._userId, self._page[0], self._page[1]))

class RecordListButton_Next(disnake.ui.Button):
	def __init__(self, discordId: int, userId: int, page: list[int]):
		super().__init__(
			style=disnake.ButtonStyle.blurple,
			emoji="▶️",
			disabled=True if page[0]+1==page[1] else False,
		)
		self._userId = userId
		self._page = page[0]+1
		self._discordId = discordId
	
	async def callback(self, i: disnake.Interaction):
		if self._discordId != i.user.id:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)
			return
		record = await getRecord(self._userId, self._page)
		await i.response.edit_message(view=RecordListView(i.user.id, await getRecordOptions(record['result'], i), self._userId, record['page']))

class RecordListButton_Update(disnake.ui.Button):
	def __init__(self, discordId: int, userId: int, disabled: bool = False):
		if disabled:
			super().__init__(
				style=disnake.ButtonStyle.gray,
				label="갱신 완료",
				disabled=True,
				row=2
			)
		else:
			super().__init__(
				style=disnake.ButtonStyle.green,
				emoji="♻",
				label="플레이어 갱신",
				row=2
			)
		self._userId = userId
		self._discordId = discordId
	
	async def callback(self, i: disnake.Interaction):
		if self._discordId == i.user.id:
			await i.response.defer()
			async with aiohttp.ClientSession(headers=AYAGG_HEADER) as session:
				async with session.post(AYAGG_API_URL + f"/player/{self._userId}/update") as res:
					if res.status != 200:
						await i.edit_original_message(embed=makeErrorEmbed(f"갱신에 실패했어요.\n잠시 뒤에 다시 시도하거나 [aya.gg](https://aya.gg/)에서 갱신해주세요!"))
						return
			record = await getRecord(self._userId)
			await i.edit_original_message(view=RecordListView(i.user.id, await getRecordOptions(record['result'], i), self._userId, record['page'], True))
		else:
			await i.response.send_message(embed=makeErrorEmbed("선택권은 메시지 주인에게만 있어요!"), ephemeral=True)

class RecordListView(disnake.ui.View):
	def __init__(self, discordId: int, options: list[disnake.SelectOption], userId: int, page: list[int], updated: bool = False):
		super().__init__(timeout=None)
		self.add_item(RecordList(discordId, userId, options))
		self.add_item(RecordListButton_Previous(discordId, userId, page))
		self.add_item(RecordListButton_NowPage(discordId, userId, page))
		self.add_item(RecordListButton_Next(discordId, userId, page))
		self.add_item(RecordListButton_Update(discordId, userId, updated))

def setup(bot: commands.Bot):
	bot.add_cog(Stat(bot))