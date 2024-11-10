import time, disnake, requests
from disnake.ext import commands
from config import AYAGG_API_URL, AYAGG_HEADER

async def getERARStatus():
	start = time.time()*1000
	req = requests.get(AYAGG_API_URL + '/status', headers=AYAGG_HEADER)
	end = time.time()*1000
	r = req.json()
	return ["정상" if r['erar'] == "FINE" else "⚠️ 점검 중!", "정상" if r['errr'] == "FINE" else "⚠️ 점검 중!", end-start]

class Info(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		
	@commands.slash_command(
		name=disnake.Localized(
			"info",
			data={
				disnake.Locale.ko: "정보",
				disnake.Locale.en_US: "info"
			}
		),
		description=disnake.Localized(
			"Check the information on IHAHBOT.",
			data={
				disnake.Locale.ko: "이하봇의 정보를 확인해요.",
				disnake.Locale.en_US: "Check the information on IHAHBOT."
			}
		)
	)
	async def nowPlayer_slashCommands(
		self, i: disnake.CommandInteraction
	):
		embed = disnake.Embed(
			title="이하봇 정보",
			color=0xabcdef
		)
		embed.add_field(name="서버 수", value=f"{len(self.bot.guilds)}개")
		embed.add_field(name="개발자", value="라이니 `@rai_ny._.`\n741973166364164099")
		await i.response.send_message(embed=embed)

	@commands.slash_command(
		name=disnake.Localized(
			"ping",
			data={
				disnake.Locale.ko: "핑",
				disnake.Locale.en_US: "ping"
			}
		),
		description=disnake.Localized(
			"Check the network delay status and API server status.",
			data={
				disnake.Locale.ko: "네트워크 지연 상태와 API 서버 상태를 확인해요.",
				disnake.Locale.en_US: "Check the network delay status and API server status."
			}
		)
	)
	async def nowPlayer_slashCommands(
		self, i: disnake.CommandInteraction
	):
		erarStatus = await getERARStatus()
		embed = disnake.Embed(
			title="데이터 서버 상태 및 레이턴시",
			color=0xabcdef
		)
		embed.add_field(name="Discord", value=f"정상\n`{int(self.bot.latency*1000)}ms`")
		embed.add_field(name="AYA.GG", value=f"{erarStatus[0]}\n`{int(erarStatus[2])}ms`")
		embed.add_field(name="이터널 리턴", value=erarStatus[1])
		embed.set_footer(text="지연 시간의 기준점은 이하봇 서버입니다.")
		await i.response.send_message(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(Info(bot))