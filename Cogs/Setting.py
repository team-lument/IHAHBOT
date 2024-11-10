import disnake
from disnake.ext import commands
from module.embed import makeErrorEmbed
from module.player import getUserId, getUserLevel
from module.setting import setMemberSetting

class Setting(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(
		name=disnake.Localized(
			"setting",
			data={
				disnake.Locale.ko: "설정",
				disnake.Locale.en_US: "setting"
			}
		),
		description=disnake.Localized(
			"Setting your IHAHBOT experience.",
			data={
				disnake.Locale.ko: "이하봇을 설정해요.",
				disnake.Locale.en_US: "Setting your IHAHBOT experience."
			}
		),
		options=[
			disnake.Option(
				type=disnake.OptionType.string,
				name="key",
				description="Setting key.",
				choices=[
					disnake.OptionChoice(
						name=disnake.Localized(
							"Language",
							data={
								disnake.Locale.ko: "언어",
								disnake.Locale.en_US: "Language"
							}
						),
						value="locale"
					),
					disnake.OptionChoice(
						name=disnake.Localized(
							"Hide Nickname",
							data={
								disnake.Locale.ko: "닉네임 가리기",
								disnake.Locale.en_US: "Hide Nickname"
							}
						),
						value="hideNick"
					),
					disnake.OptionChoice(
						name=disnake.Localized(
							"Hide Game ID",
							data={
								disnake.Locale.ko: "게임 ID 가리기",
								disnake.Locale.en_US: "Hide Game ID"
							}
						),
						value="hideGameId"
					),
					disnake.OptionChoice(
						name=disnake.Localized(
							"My Eternal Return Nickname",
							data={
								disnake.Locale.ko: "내 이터널 리턴 닉네임",
								disnake.Locale.en_US: "My Eternal Return Nickname"
							}
						),
						value="gameNickname"
					)
				],
				required=True
			),
			disnake.Option(
				type=disnake.OptionType.string,
				name="value",
				description="Setting value.",
				required=True,
				autocomplete=True
			)
		]
	)
	async def setting_slashCommand(
		self, i: disnake.CommandInteraction,
		key: str, value: str
	):
		if key == "locale":
			await i.response.send_message(embed=makeErrorEmbed("아직 준비 중인 기능이에요."), ephemeral=True)
			return
		elif key == "hideNick":
			if value == "true" or value == "false":
				setMemberSetting(i.user.id, i.guild.id, key, value)
				embed = disnake.Embed(
					title=":white_check_mark: 설정 성공",
					description=f"`{i.guild.name}` 서버의 `닉네임 가리기` 설정을 **{'켰어요' if value == "true" else '껐어요'}**."
				)
				await i.response.send_message(embed=embed, ephemeral=True)
				return
			else:
				await i.response.send_message(embed=makeErrorEmbed("잘못된 값이에요."), ephemeral=True)
				return
		elif key == "hideGameId":
			if value == "true" or value == "false":
				setMemberSetting(i.user.id, i.guild.id, key, value)
				embed = disnake.Embed(
					title=":white_check_mark: 설정 성공",
					description=f"`{i.guild.name}` 서버의 `게임 ID 가리기` 설정을 **{'켰어요' if value == "true" else '껐어요'}**."
				)
				await i.response.send_message(embed=embed, ephemeral=True)
				return
			else:
				await i.response.send_message(embed=makeErrorEmbed("잘못된 값이에요."), ephemeral=True)
				return
		elif key == "gameNickname":
			# await i.response.send_message(embed=makeErrorEmbed("아직 준비 중인 기능이에요."), ephemeral=True)
			# return
			userId = await getUserId(value)
			level = await getUserLevel(userId)
			embed = disnake.Embed(
				title="👤 계정 확인",
				description=f"`{i.guild.name}` 서버의 `내 이터널 리턴 닉네임` 설정을 **{value}** (Lv.{level}) 로 변경해요.\n정말 내 이터널 리턴 닉네임이 맞나요? **__다를 경우 이하봇 이용이 중지될 수 있어요.__**"
			)
			await i.response.send_message(embed=embed, ephemeral=True)

def setup(bot: commands.Bot):
	bot.add_cog(Setting(bot))