import disnake, os, asyncio, platform, logging, coloredlogs
from disnake.ext import commands
from config import *

bot = commands.AutoShardedBot(shard_count=1, command_prefix=commands.when_mentioned, test_guilds=[742188157424107679,812664224512868382] if f"{platform.system()}" == "Windows" else None)
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

@bot.event
async def on_shard_connect(shard_id):
	logger.info(f"Shard #{shard_id} is ready!")

@bot.event
async def on_shard_disconnect(shard_id):
	logger.error(f"Shard #{shard_id} is stopped.")

@bot.event
async def on_slash_command(i: disnake.CommandInteraction):
	options = ""
	for x in i.data.options:
		options = f"{options} [{x.name}:{x.value}]"
	#await logDB(f"{i.user.name}", i.user.id, i.guild.id, i.channel.id, f"/{i.data.name} {options[1:]}")
	logger.debug(f"useSlashCommand | @{i.user.name} ({i.user.id}) | /{i.data.name} {options[1:]} | {i.guild.id} # {i.channel.id}")

@bot.slash_command(
	name="logout",
	description="Bot Logout",
	guild_ids=[742188157424107679]
)
async def reload_slashCommand(i: disnake.CommandInteraction):
	await bot.close()

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

async def change_presence(shard_id):
	if not "-working" in version:
		shard = bot.get_shard(shard_id)
		while not shard.is_closed():
			await bot.change_presence(status = disnake.Status.online, activity = disnake.Game(f"{version.split('-')[0]} / Shard #{shard_id}"))
			await asyncio.sleep(15)
			await bot.change_presence(status = disnake.Status.online, activity = disnake.Activity(type=disnake.ActivityType.listening, name="/help"))
			await asyncio.sleep(15)
			await bot.change_presence(status = disnake.Status.online, activity = disnake.Game(f"{len(bot.guilds)} Guilds"))
			await asyncio.sleep(15)
	else:
		await bot.change_presence(status = disnake.Status.online, activity = disnake.Game(f"IHAHBOT is working!"))

if f"{platform.system()}" != "Windows": bot.run(TOKEN_PRODUCTION)
else: bot.run(TOKEN_TESTBUILD)