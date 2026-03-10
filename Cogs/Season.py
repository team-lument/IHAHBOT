import disnake, aiohttp, json, datetime, time
from config import API_URL, API_HEADER
from disnake.ext import commands
from module.embed import makeErrorEmbed
from module.variables import getSeason

class Season(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(
		name=disnake.Localized(
			"season",
			data={
				disnake.Locale.ko: "시즌",
				disnake.Locale.en_US: "season"
			}
		),
		description=disnake.Localized(
			"Get the remaining rank season time.",
			data={
				disnake.Locale.ko: "남은 랭크 시즌 시간을 출력해요.",
				disnake.Locale.en_US: "Get the remaining rank season time."
			}
		)
	)
	async def season_slashCommand(
		self, i: disnake.CommandInteraction
	):
		async with aiohttp.ClientSession(headers=API_HEADER) as session:
			async with session.get(API_URL + f"/v2/data/Season") as req:
				r = json.loads(await req.text())
				if r['code'] != 200:
					await i.response.send_message(embed=makeErrorEmbed(f"API 요청에 실패했어요. `({r['code']})`\n-# /정보 명령어를 통해 현재 서버 상황을 확인할 수 있어요."))
					return
		nowSeason = 0
		for x in r['data']: nowSeason = x['seasonID'] if x['isCurrent'] == True else nowSeason
		seasonEndTime = str(r['data'][nowSeason]['seasonEnd'])
		startTime = datetime.datetime.strptime(r['data'][nowSeason]['seasonStart'], "%Y-%m-%d %H:%M:%S")
		endTime = datetime.datetime.strptime(seasonEndTime, "%Y-%m-%d %H:%M:%S")
		progress = ((datetime.datetime.now() - startTime) / (endTime - startTime)) * 100
		progress = max(0, min(progress, 100))

		remain_time = endTime - datetime.datetime.now()
		embed = disnake.Embed(
			title=f"{getSeason(nowSeason)}",
			description=f"{progress:.2f}% 진행됨",
			color=0x00ff00
		)
		embed.add_field(name="시즌 종료", value=f"{endTime.strftime('%y-%m-%d %H:%M')} (KST)")
		embed.add_field(name="남은 시간", value=f"{remain_time.days}일 {remain_time.seconds//3600}시간 {(remain_time.seconds//60)%60}분 {remain_time.seconds%60}초")
		embed.set_footer(text="이하봇 • 팀 루멘트가 ♥️로 제작")
		await i.response.send_message(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(Season(bot))