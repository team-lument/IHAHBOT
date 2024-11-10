import disnake, aiohttp
from disnake.ext import commands

async def getNowPlayers():
	async with aiohttp.ClientSession() as session:
		async with session.get("https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?&appid=1049590") as req:
			r = await req.json()
			now = r['response']['player_count']
		async with session.get("https://steamcharts.com/app/1049590") as req:
			r = await req.text()
			daypeak = r.replace("\t", "").replace("\n", "").split('</span><br>24-hour peak')[0].split('<span class="num">')[-1]
	return ['{:,}'.format(now),'{:,}'.format(int(daypeak))]

class Concurrent(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(
		name=disnake.Localized(
			"ccu",
			data={
				disnake.Locale.ko: "동접",
				disnake.Locale.en_US: "ccu"
			}
		),
		description=disnake.Localized(
			"Check number of current users in Eternal Return of Steam.",
			data={
				disnake.Locale.ko: "이터널 리턴 스팀 동접을 확인해요.",
				disnake.Locale.en_US: "Check number of current users in Eternal Return of Steam."
			}
		)
	)
	async def nowPlayer_slashCommands(
		self, i: disnake.CommandInteraction
	):
		np = await getNowPlayers()
		embed = disnake.Embed(
			title="동시 접속자 수",
			color=0xabcdef
		)
		embed.add_field(name="현재", value=f"{np[0]}명")
		embed.add_field(name="24h 최고", value=f"{np[1]}명")
		embed.set_footer(text="'24h 최고'의 경우 갱신 시점에 따라 차이가 있을 수 있어요.")
		await i.response.send_message(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(Concurrent(bot))