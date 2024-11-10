import disnake
from disnake.ext import commands
from module.embed import helpEmbed, helpEmbed2, SpecialThanks

def getHelpEmbed(page: int):
	if page == 1: return helpEmbed()
	elif page == 2: return helpEmbed2()
	elif page == 3: return SpecialThanks()

class HelpLeft(disnake.ui.Button['HelpView']):
	def __init__(self, page: int):
		disabled = False
		if page <= 1:
			disabled = True
		super().__init__(emoji="◀️", style=disnake.ButtonStyle.blurple, disabled=disabled)
		self._page = page-1
	
	async def callback(self, i: disnake.Interaction):
		await i.response.edit_message(embed=getHelpEmbed(self._page), view=HelpView(self._page))

class HelpRight(disnake.ui.Button['HelpView']):
	def __init__(self, page: int, text: bool = False):
		disabled = False
		if page >= 3:
			disabled = True
		super().__init__(emoji="▶️", style=disnake.ButtonStyle.blurple, disabled=disabled)
		self._page = page+1
		self._text = text
	
	async def callback(self, i: disnake.Interaction):
		await i.response.edit_message(embed=getHelpEmbed(self._page), view=HelpView(self._page))

class HelpView(disnake.ui.View):
	def __init__(
		self,
		page: int = 1
	):
		super().__init__(timeout=None)
		self.add_item(HelpLeft(page))
		self.add_item(disnake.ui.Button(label=f"{page} / 3", disabled=True, style=disnake.ButtonStyle.gray))
		self.add_item(HelpRight(page))

class Help(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.slash_command(
		name=disnake.Localized(
			"help",
			data={
				disnake.Locale.ko: "도움말",
				disnake.Locale.en_US: "help"
			}
		),
		description=disnake.Localized(
			"Send help message.",
			data={
				disnake.Locale.ko: "도움말을 전송해요.",
				disnake.Locale.en_US: "Send help message."
			}
		),
	)
	async def help_slashCommands(
		self, i: disnake.CommandInteraction
	):
		embed=helpEmbed()
		await i.response.send_message(embed=embed, view=HelpView(page=1), ephemeral=True)

def setup(bot: commands.Bot):
	bot.add_cog(Help(bot))