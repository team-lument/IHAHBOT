import os, disnake
from disnake.ext import commands
from module.database import getAllCharacterName, getCharacterFullName, getCharacterName, getCharacterPrice, getCharacterStory, getSkinName, getSkinVariable, getSkinType, makeSkinList, searchCharacterName
from module.embed import makeErrorEmbed

skinTypeOptions = {
	"FREE": "캐릭터 구매 시 기본 지급",
	"SEASON": "__{1} 시즌 {0}__ 랭크 티어 보상",
	"PASS": "**ER PASS** __{1} 시즌 {0}__ {2} 레벨 보상",
	"PASS_1st": "__1주년 패스__ {2} 레벨 보상",
	"PACK": "**시즌 팩** 시즌 {0} 구매자 한정",
	"NOW": "GeForce Now 구독하기",
	"NEWSLETTER": "뉴스레터 Vol.{0} 구독하기",
	"EVENT": "{1} 이벤트",
	"EVENT_LINK": "[{1} 이벤트]({2})",
	"EVENT_ATTEND": "EA 시즌 9 출석부 이벤트 {0}월 10일차 보상",
	"EXCHANGE": "{2} 토큰 교환소에서 {0} 토큰으로 교환",
	"S_EXCHANGE": "정규 시즌 {0} 토큰 교환소에서 450 토큰으로 교환"
}

class SkinView(disnake.ui.View):
	def __init__(self, skinList: list[disnake.SelectOption], characterId):
		super().__init__()
		self.add_item(Skin(skinList))
		self.add_item(ChangeView_Character(characterId))
		self.add_item(ChangeView_Story(characterId))

class Skin(disnake.ui.Select):
	def __init__(self, skinList: list[disnake.SelectOption]):
		self._skinList = skinList
		super().__init__(placeholder="스킨을 선택해주세요.", options=skinList)

	async def callback(self, i: disnake.MessageInteraction):
		await i.response.defer()
		characterId = i.values[0].split("@")[0]
		skinId = int(i.values[0].split("@")[1])
		var = await getSkinVariable(skinId)
		skinType = await getSkinType(skinId)
		embed = disnake.Embed(
			title=await getSkinName(skinId)
		)
		if skinType == "SHOP" and var > 0:
			embed.add_field(name="주요 획득 경로", value=f"<:NP:1264438465546682380> `{'{:,}'.format(await getSkinVariable(skinId))}`\n-# 가격은 차이가 있을 수 있어요.\n-# 일부 스킨은 제작소에서도 획득할 수 있어요.", inline=False)
		elif skinType:
			var0 = await getSkinVariable(skinId, 0)
			var1 = await getSkinVariable(skinId, 1)
			var2 = await getSkinVariable(skinId, 2)
			embed.add_field(name="주요 획득 경로", value=f"{skinTypeOptions[skinType].replace('{0}', f'{var0}').replace('{1}', f'{var1}').replace('{2}', f'{var2}')}\n-# 획득 경로 및 가격은 차이가 있을 수 있어요.\n-# 일부 스킨은 제작소에서도 획득할 수 있어요.", inline=False)
		else:
			embed.add_field(name="주요 획득 경로", value="없음\n-# 일부 스킨은 제작소에서도 획득할 수 있어요.")
		embed.set_image(url=f"https://aya.gg/images/characters/CharFull_{(await getCharacterName(characterId, 'en')).replace(' ', '').replace('&', '')}_S{str(skinId)[4:7]}.webp")
		await i.edit_original_message(embed=embed, view=SkinView(self._skinList, characterId))

class ChangeView_Skin(disnake.ui.Button):
	def __init__(self, skinList: list[disnake.SelectOption], characterId: int):
		self._skinList = skinList
		self._character = characterId
		super().__init__(style=disnake.ButtonStyle.primary, label="스킨 보기")

	async def callback(self, i: disnake.MessageInteraction):
		embed = disnake.Embed(
			title=await getCharacterName(self._character),
			description="스킨을 선택해주세요."
		)
		await i.response.edit_message(embed=embed, view=SkinView(self._skinList, self._character), attachments=None)

class ChangeView_Story(disnake.ui.Button):
	def __init__(self, characterId: int):
		self._characterId = characterId
		super().__init__(style=disnake.ButtonStyle.primary, label="스토리 보기")

	async def callback(self, i: disnake.MessageInteraction):
		characterName = await getCharacterName(self._characterId, "en")
		fullName = await getCharacterFullName(self._characterId)
		story = await getCharacterStory(self._characterId)
		embed = disnake.Embed(
			title=fullName,
			description=f"**\"{story[0]}\"**\n\n{story[1].replace('{{n}}', '\n')}"
		)
		embed.set_image(file=disnake.File(fp=f"image/CharacterInfo/{characterName}.png", filename=f"IHBv4_ER_{characterName}_Background.png"))
		await i.response.edit_message(embed=embed, view=StoryView(await makeSkinList(self._characterId), self._characterId))

class ChangeView_Character(disnake.ui.Button):
	def __init__(self, characterId: int):
		self._characterId = characterId
		super().__init__(style=disnake.ButtonStyle.primary, label="실험체 보기")

	async def callback(self, i: disnake.MessageInteraction):
		characterName = await getCharacterName(self._characterId, "en")
		[np, acoin] = await getCharacterPrice(self._characterId)
		story = await getCharacterStory(self._characterId)
		embed = disnake.Embed(
			title=await getCharacterName(self._characterId),
			description=f"**\"{story[0]}\"**"
		)
		embed.add_field(name="상점 가격", value=f"<:NP:1264438465546682380> `{'{:,}'.format(np)}`\n<:ACoin:1264438301662646284> `{'{:,}'.format(acoin)}`\n-# 상점 가격은 차이가 있을 수 있어요.\n-# 일부 아이템은 제작소에서도 획득할 수 있어요.", inline=False)
		if os.path.isfile(f"image/skinFull/{characterName}_0.png"):
			embed.set_image(file=disnake.File(fp=f"image/skinFull/{characterName}_0.png", filename=f"IHBv4_ERData_{characterName}_Skin_0_Full.png"))
		else:
			embed.set_image(url=f"https://aya.gg/images/characters/SkinFull_{characterName}_S000.webp")
		await i.response.edit_message(embed=embed, view=CharacterView(await makeSkinList(self._characterId), self._characterId))

class StoryView(disnake.ui.View):
	def __init__(self, skinList: list[disnake.SelectOption], characterId: int):
		super().__init__()
		self.add_item(ChangeView_Character(characterId))
		self.add_item(ChangeView_Skin(skinList, characterId))

class CharacterView(disnake.ui.View):
	def __init__(self, skinList: list[disnake.SelectOption], characterId: int):
		super().__init__()
		self.add_item(ChangeView_Story(characterId))
		self.add_item(ChangeView_Skin(skinList, characterId))

class Database(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(
		name=disnake.Localized(
			"database",
			data={
				disnake.Locale.ko: "데이터베이스",
				disnake.Locale.en_US: "database"
			}
		),
		description=disnake.Localized(
			"Database commands.",
			data={
				disnake.Locale.ko: "데이터베이스 명령어의 모음입니다.",
				disnake.Locale.en_US: "Database commands."
			}
		)
	)
	async def database_slashCommand(self, i: disnake.CommandInteraction):
		pass

	@database_slashCommand.sub_command(
		name=disnake.Localized(
			"character",
			data={
				disnake.Locale.ko: "실험체",
				disnake.Locale.en_US: "character"
			}
		),
		description=disnake.Localized(
			"Get character information from IHAHBOT database.",
			data={
				disnake.Locale.ko: "이하봇 데이터베이스에서 실험체 정보를 불러옵니다.",
				disnake.Locale.en_US: "Get character information from IHAHBOT database."
			}
		),
		options=[
			disnake.Option(
				type=disnake.OptionType.number,
				name=disnake.Localized(
					"name",
					data={
						disnake.Locale.ko: "이름",
						disnake.Locale.en_US: "name"
					}
				),
				description=disnake.Localized(
					"Character name.",
					data={
						disnake.Locale.ko: "실험체 이름.",
						disnake.Locale.en_US: "Character name."
					}
				),
				required=True,
				autocomplete=True
			)
		]
	)
	async def database_character_slashCommands(
		self, i: disnake.CommandInteraction, name: int
	):
		name = int(name)
		characterName = await getCharacterName(name, "en")
		if not "character" in characterName:
			await i.response.defer()
			[np, acoin] = await getCharacterPrice(name)
			story = await getCharacterStory(name)
			embed = disnake.Embed(
				title=await getCharacterName(name),
				description=f"**\"{story[0]}\"**"
			)
			embed.add_field(name="상점 가격", value=f"<:NP:1264438465546682380> `{'{:,}'.format(np)}`\n<:ACoin:1264438301662646284> `{'{:,}'.format(acoin)}`\n-# 상점 가격은 차이가 있을 수 있어요.\n-# 일부 아이템은 제작소에서도 획득할 수 있어요.", inline=False)
			if os.path.isfile(f"image/skinFull/{characterName}_0.png"):
				embed.set_image(file=disnake.File(fp=f"image/skinFull/{characterName}_0.png", filename=f"IHBv4_ERData_{characterName}_Skin_0_Full.png"))
			else:
				embed.set_image(url=f"https://aya.gg/images/characters/SkinFull_{characterName}_S000.webp")
			await i.edit_original_message(embed=embed, view=CharacterView(await makeSkinList(name), name))
		else:
			await i.response.send_message(embed=makeErrorEmbed("그런 실험체는 없어요."), ephemeral=True)
	
	@database_character_slashCommands.autocomplete("name")
	async def database_character_autocomplete(
		self, i: disnake.CommandInteraction, name: str
	):
		res=[]
		if name == "" or name is None:
			cn = await getAllCharacterName("ko")
		else:
			cn = await searchCharacterName(name, "ko")
		for x in range(len(cn) if len(cn) < 25 else 25):
			res.append(disnake.OptionChoice(name=cn[x][1], value=cn[x][0]))
		return res

def setup(bot: commands.Bot):
	bot.add_cog(Database(bot))