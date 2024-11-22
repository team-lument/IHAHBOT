import disnake, os, platform, logging, coloredlogs, asyncio
from disnake.ext import commands
from koreanbots import KoreanbotsRequester
from config import *
from module.log import logDB

bot = commands.Bot(command_prefix=commands.when_mentioned, test_guilds=[742188157424107679,812664224512868382] if f"{platform.system()}" == "Windows" else None)
bot.remove_command('help')

logger = logging.getLogger("ihahbot.main")
coloredlogs.install(level='DEBUG', logger=logger, fmt='%(asctime)s | %(levelname)s | %(message)s')

for filename in os.listdir("Cogs"):
	if filename.endswith(".py"):
		try:
			bot.load_extension(f"Cogs.{filename[:-3]}")
			logger.info(f"Module loaded: {filename}")
		except Exception as e:
			logger.error(f"Module load failed: {filename} - {e}")

@bot.event
async def on_ready():
	logger.info(f"Woke Up! {bot.user.name} ({bot.user.id})")
	await bot.change_presence(status = disnake.Status.online, activity = disnake.CustomActivity(name=f"No.1 이터널 리턴 전적봇 | /전적", state="No.1 이터널 리턴 전적봇 | /전적", emoji=disnake.PartialEmoji(name="rank1", id=1284775535855140916)))

async def update_bot_info():
	await bot.wait_until_ready()
	while not bot.is_closed():
		await KoreanbotsRequester(KOREANBOTS_TOKEN).post_update_bot_info(bot.user.id, servers=len(bot.guilds))
		logger.info(f"koreanbots | Guilds: {len(bot.guilds)}")
		await asyncio.sleep(60)

bot.loop.create_task(update_bot_info())

@bot.event
async def on_slash_command(i: disnake.CommandInteraction):
	options = ""
	for x in i.data.options:
		options = f"{options} [{x.name}:{x.value}]" if x.value != None else f"{options} {x.name}"
	await logDB(f"{i.user.name}", i.user.id, i.guild.id, i.channel.id, f"/{i.data.name} {options[1:]}")
	logger.debug(f"useSlashCommand | @{i.user.name} ({i.user.id}) | /{i.data.name} {options[1:]} | {i.guild.id} # {i.channel.id}")

@bot.slash_command(
	name="reload",
	description="Reload the module.",
	options=[
		disnake.Option(
			type=3,
			name="module",
			description="Module name.",
			required=True
		)
	],
	guild_ids=[742188157424107679]
)
async def reload_slashCommand(i: disnake.CommandInteraction, module: str):
	try:
		bot.reload_extension(f"Cogs.{module}")
		await i.response.send_message(f"Module reloaded: {module}")
	except Exception as e:
		await i.response.send_message(f"Module reload failed: {module}\n```{e}```")

@bot.slash_command(
	name="unload",
	description="Unload the module.",
	options=[
		disnake.Option(
			type=3,
			name="module",
			description="Module name.",
			required=True
		)
	],
	guild_ids=[742188157424107679]
)
async def unload_slashCommand(i: disnake.CommandInteraction, module: str):
	try:
		bot.unload_extension(f"Cogs.{module}")
		await i.response.send_message(f"Module unloaded: {module}")
	except Exception as e:
		await i.response.send_message(f"Module unload failed: {module}\n```{e}```")

@bot.slash_command(
	name="load",
	description="Load the module.",
	options=[
		disnake.Option(
			type=3,
			name="module",
			description="Module name.",
			required=True
		)
	],
	guild_ids=[742188157424107679]
)
async def load_slashCommand(i: disnake.CommandInteraction, module: str):
	try:
		bot.load_extension(f"Cogs.{module}")
		await i.response.send_message(f"Module loaded: {module}")
	except Exception as e:
		await i.response.send_message(f"Module load failed: {module}\n```{e}```")

if f"{platform.system()}" != "Windows": bot.run(TOKEN_PRODUCTION)
else: bot.run(TOKEN_TESTBUILD)