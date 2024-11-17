import disnake
from module.embed import routeEmbed
from module.route import getRoute
from disnake.ext import commands

class Route(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(
		name=disnake.Localized(
			"route",
			data={
				disnake.Locale.ko: "루트"
			}
		),
		description=disnake.Localized(
			"Check the route information.",
			data={
				disnake.Locale.ko: "루트 정보를 확인해보세요."
			}
		)
	)
	async def freecharacter_slashCommmands(
		self, i: disnake.CommandInteraction,
		route: str = commands.Param(
			name="route",
			description="Enter the route ID or route name for search."
		)
	):
		if route.isdigit():
			data = await getRoute(id=int(route))
			await i.response.send_message(embed=routeEmbed(data['result']))
		else:
			data = await getRoute(name=route)

def setup(bot: commands.Bot):
	bot.add_cog(Route(bot))