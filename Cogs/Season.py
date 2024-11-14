import disnake, aiohttp, json, datetime, time
from config import API_URL, API_HEADER
from disnake.ext import commands
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
			async with session.get(API_URL[:-3] + f"/v2/data/Season") as req:
				r = json.loads(await req.text())
		nowSeason = 0
		for x in r['data']: nowSeason = x['seasonID'] if x['isCurrent'] == True else nowSeason
		endtime = datetime.datetime.strptime(str(r['data'][nowSeason]['seasonEnd']), "%Y-%m-%d %H:%M:%S")
		embed = disnake.Embed(
			title="남은 시즌 기간",
			description=f"{getSeason(nowSeason)}"
		)
		embed.add_field(name="종료 일시", value=f"<t:{int(time.mktime(endtime.timetuple()))}:F>\n<t:{int(time.mktime(endtime.timetuple()))}:R>")
		embed.set_footer(text="표기 종료 일시는 현재 본인의 시간대로 표시됩니다.")
		await i.response.send_message(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(Season(bot))