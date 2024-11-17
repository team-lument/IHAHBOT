import datetime
from config import LOG_WEBHOOK_URL
from discord_webhook import DiscordWebhook, DiscordEmbed

async def logDB(user: str = "dummy", userId: int = 0, serverId: int = 0, channelId: int = 0, cmd: str = "Unknown Command"):
	webhook = DiscordWebhook(LOG_WEBHOOK_URL)
	embed = DiscordEmbed(title="📜 v4 명령어 로그")
	embed.add_embed_field(name="유저", value=f"<@{userId}>\n`{user}` `({userId})`")
	embed.add_embed_field(name="서버", value=f"[{serverId}](https://discord.com/channels/{serverId})")
	embed.add_embed_field(name="채널", value=f"{channelId}\n<#{channelId}>")
	embed.add_embed_field(name="명령어", value=f"`{cmd}`", inline=False)
	embed.add_embed_field(name="서버상 시간", value=f"`{datetime.datetime.now()}`", inline=False)
	embed.set_timestamp()
	webhook.add_embed(embed)
	webhook.execute()