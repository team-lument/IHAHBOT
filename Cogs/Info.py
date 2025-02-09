import time, disnake, requests
from disnake.ext import commands
from config import API_HEADER, API_URL, AYAGG_API_URL, AYAGG_HEADER
from module.variables import getVersion

async def getStatus():
	result = {}
	try:
		erar_start = time.time()*1000
		req = requests.get(AYAGG_API_URL + '/status', headers=AYAGG_HEADER)
		erar_end = time.time()*1000; erar = req.json()
		result["erar"] = ["정상" if erar['erar'] == "FINE" else "⚠️ 점검 중!" if req.status_code != 200 else f"❌ 이용 불가 `({erar.status_code})`", erar_end-erar_start]
	except:
		erar = {'errr': None}
		result["erar"] = ["❌ 이용 불가 `(알 수 없음)`", 0]
	try:
		errr_start = time.time()*1000
		req = requests.get(API_URL + f'/v1/freeCharacters/2', headers=API_HEADER)
		errr_end = time.time()*1000; errr = req.json()
		if errr['code'] != 200 or len(errr['freeCharacters']) == 0: result["errr"] = [f"❌ 이용 불가 `(점검 중)`", errr_end-errr_start]
		else: result["errr"] = ["정상" if erar['errr'] == "FINE" else "⚠️ 점검 중!", errr_end-errr_start]
	except:
		result["errr"] = ["❌ 이용 불가 `(알 수 없음)`", 0]
	return result

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
		infoEmbed.add_field(name="버전", value=f"{getVersion()}", inline=False)
		infoEmbed.add_field(name="서버 수", value=f"{len(self.bot.guilds)}개")
		infoEmbed.add_field(name="개발자", value="라이니 `@rai_ny._.`\n741973166364164099\n이터널 리턴 [`샨티`](https://aya.gg/ko/players/샨티)")
		status = await getStatus(); erar = status["erar"]; errr = status["errr"]
		pingEmbed = disnake.Embed(
			title="데이터 서버 상태 및 레이턴시",
			color=0xabcdef
		)
		pingEmbed.add_field(name="Discord", value=f"정상\n`{int(self.bot.latency*1000)}ms`")
		pingEmbed.add_field(name="AYA.GG", value=f"{erar[0]}\n{f'`{int(erar[1])}ms`' if erar[1] != 0 else ''}")
		pingEmbed.add_field(name="이터널 리턴", value=f"{errr[0]}\n{f'`{int(errr[1])}ms`' if errr[1] != 0 else ''}")
		pingEmbed.set_footer(text="지연 시간의 기준점은 이하봇 서버입니다.")
		await i.edit_original_message(embeds=[infoEmbed, pingEmbed])

def setup(bot: commands.Bot):
	bot.add_cog(Info(bot))