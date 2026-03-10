import disnake, aiohttp, json
from config import API_URL, API_HEADER
from module.database import getCharacterName
from module.embed import makeErrorEmbed
from module.setting import getMemberSetting
from disnake.ext import commands

class Rotation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(
		name=disnake.Localized(
			"rotation",
			data={
				disnake.Locale.ko: "로테이션",
				disnake.Locale.en_US: "rotation"
			}
		),
		description=disnake.Localized(
			"Check out the characters available for free this week.",
			data={
				disnake.Locale.ko: "이번 주에 무료로 이용할 수 있는 실험체를 확인해보세요.",
				disnake.Locale.en_US: "Check out the characters available for free this week."
			}
		)
	)
	async def freecharacter_slashCommmands(
		self, i: disnake.CommandInteraction
	):
		embed = disnake.Embed(
			title=f"일주일 무료 실험체"
		).set_footer(text="이하봇 • 팀 루멘트가 ♥️로 제작")
		async with aiohttp.ClientSession(headers=API_HEADER) as session:
			async with session.get(API_URL + f'/v1/freeCharacters/2') as req:
				r = json.loads(await req.text()); characterName = []
				if r['code'] != 200:
					for x in r['freeCharacters']: characterName.append(getCharacterName(x, getMemberSetting(i.user.id, i.guild.id, "locale")))
				else:
					characterName = ["❌ API 요청에 실패했어요.\n-# /정보 명령어를 통해 현재 서버 상황을 확인할 수 있어요."]
				embed.add_field(name="루미아 섬", value=f"{', '.join(characterName)}", inline=False)
			async with session.get(API_URL + f'/v1/freeCharacters/6') as req:
				r = json.loads(await req.text()); characterName = []
				if r['code'] == 200:
					for x in r['freeCharacters']: characterName.append(getCharacterName(x, getMemberSetting(i.user.id, i.guild.id, "locale")))
				else:
					characterName = ["❌ API 요청에 실패했어요.\n-# /정보 명령어를 통해 현재 서버 상황을 확인할 수 있어요."]
				embed.add_field(name="코발트 프로토콜", value=f"{', '.join(characterName)}", inline=False)
		await i.response.send_message(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(Rotation(bot))