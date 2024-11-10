import disnake
from disnake.ext import commands

class Patchnote(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.slash_command(
		name=disnake.Localized(
			"patchnote",
			data={
				disnake.Locale.ko: "패치노트"
			}
		),
		description=disnake.Localized(
			"Get data of ER patchnotes.",
			data={
				disnake.Locale.ko: "이터널 리턴 패치노트를 가져옵니다."
			}
		)
	)
	async def patchnote_slashcommand(
		self, i: disnake.CommandInteraction
	):
		pass
		
def setup(bot: commands.Bot):
	bot.add_cog(Patchnote(bot))