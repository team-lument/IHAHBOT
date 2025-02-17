import asyncio
import disnake
from disnake.ext import commands

class TicketSystem(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message: disnake.Message):
		if message.author.bot:
			return
		if message.guild:
			if message.channel.category.id == 1340965912978915419:
				if not message.reference:
					return
				before = await message.channel.fetch_message(message.reference.message_id)
				user_id = int(message.channel.name.split('-')[-1])
				user = await self.bot.fetch_user(user_id)
				userMsg = await user.fetch_message(int(before.embeds[0].footer.text))
				await userMsg.reply(message.content)
				return
			return

		user = message.author
		guild = await self.bot.fetch_guild(911042155504631859)
		channels = await guild.fetch_channels()
		category = await guild.fetch_channel(1340965912978915419)
		ticket_name = f"이하봇-{user.id}"

		existing_channel = disnake.utils.get(channels, name=ticket_name)

		if existing_channel:
			await existing_channel.send(message.content)
			await message.add_reaction("✅")
			return

		ticket_channel = await category.create_text_channel(name=ticket_name)

		embed = disnake.Embed(
			title="🎟️ 티켓 생성됨",
			description=f"{user.mention} 님의 티켓입니다.\n\n문의 답변은 꼭 \"답장\" 기능을 이용해주세요.\n그렇지 않을 경우 봇이 메시지 인식을 할 수 없습니다.",
			color=disnake.Color.green()
		)

		embed2 = disnake.Embed(
			description=message.content
		)
		embed2.set_footer(text=f"{message.id}")

		await ticket_channel.send(content="<@&949616962869268540>", embed=embed)
		await asyncio.sleep(1)
		await ticket_channel.send(embed=embed2)
		await message.add_reaction("✅")

	@commands.slash_command(
		name="close",
		description="현재 티켓을 닫습니다.",
		guild_ids=[911042155504631859]
	)
	async def close(self, i: disnake.ApplicationCommandInteraction):
		channel = i.channel
		guild = i.guild
		category = await guild.fetch_channel(1340966118541754449)

		if not channel.name.startswith("이하봇-"):
			await i.response.send_message("❌ 이 채널은 티켓이 아닙니다!", ephemeral=True)
			return
		
		user_id = int(channel.name.split('-')[-1])
		user = await self.bot.fetch_user(user_id)
		await user.send("🚪 관리자에 의해 티켓이 닫혔습니다.")

		await channel.edit(name=f"닫힌{channel.name}", category=category)
		embed = disnake.Embed(
			title="🚪 티켓 닫힘",
			description=f"{i.user.mention}님에 의해 티켓이 닫혔습니다.",
			color=disnake.Color.red()
		)
		await channel.send(embed=embed)
		await i.response.send_message("✅ 티켓이 닫혔습니다.", ephemeral=True)

def setup(bot):
	bot.add_cog(TicketSystem(bot))
