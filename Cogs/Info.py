import time, disnake, requests
from disnake.ext import commands
from config import AYAGG_API_URL, AYAGG_HEADER

async def getERARStatus():
	try:
		start = time.time()*1000
		req = requests.get(AYAGG_API_URL + '/status', headers=AYAGG_HEADER)
		end = time.time()*1000
		if req.status_code != 200: return [f"❌ 이용 불가 `({req.status_code})`", "⚠️ 확인 불가", 0]
		r = req.json()
		return ["정상" if r['erar'] == "FINE" else "⚠️ 점검 중!", "정상" if r['errr'] == "FINE" else "⚠️ 점검 중!", end-start]
	except:
		return ["❌ 이용 불가 `(알 수 없음)`", "⚠️ 확인 불가", 0]

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
			"Check the info for IHAHBOT, network delay status and data server status.",
			data={
				disnake.Locale.ko: "이하봇의 정보, 네트워크 지연 상태와 데이터 서버 상태를 확인해요.",
				disnake.Locale.en_US: "Check the info for IHAHBOT, network delay status and data server status."
			}
		)
	)
	async def info_slashCommands(
		self, i: disnake.CommandInteraction
	):
		await i.response.defer()
		infoEmbed = disnake.Embed(
			title="이하봇 정보",
			color=0xabcdef
		)
		infoEmbed.add_field(name="버전", value="`BETA` v4.0.4 `241123` `build-13cdf86`")
		infoEmbed.add_field(name="서버 수", value=f"{len(self.bot.guilds)}개")
		infoEmbed.add_field(name="개발자", value="라이니 `@rai_ny._.`\n741973166364164099")
		erarStatus = await getERARStatus()
		pingEmbed = disnake.Embed(
			title="데이터 서버 상태 및 레이턴시",
			color=0xabcdef
		)
		pingEmbed.add_field(name="Discord", value=f"정상\n`{int(self.bot.latency*1000)}ms`")
		pingEmbed.add_field(name="AYA.GG", value=f"{erarStatus[0]}\n{f'`{int(erarStatus[2])}ms`' if erarStatus[2] != 0 else ''}")
		pingEmbed.add_field(name="이터널 리턴", value=erarStatus[1])
		pingEmbed.set_footer(text="지연 시간의 기준점은 이하봇 서버입니다.")
		await i.edit_original_message(embeds=[infoEmbed, pingEmbed])

def setup(bot: commands.Bot):
	bot.add_cog(Info(bot))