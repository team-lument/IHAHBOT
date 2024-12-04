import disnake
from disnake.ext import commands
from module.customgame import createCustomGame, deleteCustomGame, joinCustomGame, searchCustomGame
from module.player import getUserId, getUserLevel

class CustomGame_JoinCheck(disnake.ui.View):
	def __init__(self, userId: int, roomId: int):
		super().__init__()
		self._userId = userId
		self._roomId = roomId

	@disnake.ui.button(label="확인", style=disnake.ButtonStyle.green)
	async def confirm(self, btn: disnake.ui.Button, i: disnake.MessageInteraction):
		joinCustomGame(self._roomId, self._userId, i.user.id)
		await i.response.edit_message(content="✅ 참여가 완료되었어요.", embed=None, view=None)
		self.stop()

	@disnake.ui.button(label="취소", style=disnake.ButtonStyle.red)
	async def cancel(self, btn: disnake.ui.Button, i: disnake.MessageInteraction):
		await i.response.edit_message(content="참여를 취소했어요.", embed=None, view=None)
		self.stop()

class CustomGame_JoinModal(disnake.ui.Modal):
	def __init__(self, roomId: int):
		self._roomId = roomId
		super().__init__(
			title="내전 신청",
			custom_id="custom_join",
			components=[
				disnake.ui.TextInput(
					label="이터널 리턴 닉네임",
					custom_id="player",
					placeholder="이터널 리턴 닉네임을 입력해주세요.",
					min_length=2,
					max_length=16
				)
			]
		)

	async def callback(self, i: disnake.ModalInteraction):
		player = i.text_values['player']
		await i.response.defer(ephemeral=True)
		userId = await getUserId(player); userLvl = await getUserLevel(userId)
		embed = disnake.Embed(
			title="본인 확인", color=0xff0000,
			description=f"정말 **{player}**(Lv.{userLvl}) 님이 맞으신가요?\n\n**__자신이 아닌 계정, 부계정 등__** 올바르게 등록하지 않은 경우\n**__이하봇 운영정책에 의거해 이용이 제한될 수 있습니다!__**",
		)
		await i.edit_original_message(embed=embed, view=CustomGame_JoinCheck(userId=self._userId,roomId=self._roomId))

class CustomGame_JoinButton(disnake.ui.View):
	def __init__(self, roomId: int):
		super().__init__()
		self._roomId = roomId

	@disnake.ui.button(label="참가", style=disnake.ButtonStyle.green)
	async def join(self, btn: disnake.ui.Button, i: disnake.MessageInteraction):
		await i.response.send_modal(CustomGame_JoinModal(self._roomId))

class CustomGame(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(
		name=disnake.Localized(
			"custom_game",
			data={
				disnake.Locale.ko: "내전"
			}
		),
		description=disnake.Localized(
			"A collection of commands related to custom games.",
			data={
				disnake.Locale.ko: "내전에 관한 명령어 모음이예요."
			}
		)
	)
	async def customGame(
		self, i: disnake.CommandInteraction
	):
		pass

	@customGame.sub_command(
		name=disnake.Localized(
			"create",
			data={
				disnake.Locale.ko: "생성"
			}
		),
		description=disnake.Localized(
			"Create a custom game.",
			data={
				disnake.Locale.ko: "내전을 생성해요."
			}
		)
	)
	async def createCustom_slashCommand(
		self, i: disnake.CommandInteraction,
		name: str = commands.Param(
			name=disnake.Localized(
				"name",
				data={
					disnake.Locale.ko: "이름"
				}
			),
			description=disnake.Localized(
				"Custom game room name",
				data={
					disnake.Locale.ko: "내전 이름"
				}
			)
		),
		gameType: int = commands.Param(
			name=disnake.Localized(
				"type",
				data={
					disnake.Locale.ko: "종류"
				}
			),
			description=disnake.Localized(
				"custom game type (number of people per team)",
				data={
					disnake.Locale.ko: "내전 종류 (팀당 인원 수)"
				}
			),
			choices=[
				disnake.OptionChoice(
					name=disnake.Localized(
						"Lumia Island (Squad)",
						data={
							disnake.Locale.ko: "루미아 섬 (스쿼드)"
						}
					),
					value=3
				),
				disnake.OptionChoice(
					name=disnake.Localized(
						"Cobalt Protocol",
						data={
							disnake.Locale.ko: "코발트 프로토콜"
						}
					),
					value=4
				),
				disnake.OptionChoice(
					name=disnake.Localized(
						"Lumia Island (Solo)",
						data={
							disnake.Locale.ko: "루미아 섬 (솔로)"
						}
					),
					value=1
				),
				disnake.OptionChoice(
					name=disnake.Localized(
						"Lumia Island (Duo)",
						data={
							disnake.Locale.ko: "루미아 섬 (듀오)"
						}
					),
					value=2
				)
			]
		),
		open: bool = commands.Param(
			name=disnake.Localized(
				"open",
				data={
					disnake.Locale.ko: "공개"
				}
			),
			description=disnake.Localized(
				"Public? (If it's True, anyone can participate regardless of server participation.)",
				data={
					disnake.Locale.ko: "내전 공개 여부 (True 상태라면 서버 참여 여부와 관계 없이 누구나 참가할 수 있어요)"
				}
			)
		),
		open_user: bool = commands.Param(
			name=disnake.Localized(
				"blind",
				data={
					disnake.Locale.ko: "블라인드"
				}
			),
			description=disnake.Localized(
				"Disclose the information of participant? (If it's True, general users CANNOT check participants.)",
				data={
					disnake.Locale.ko: "내전 참가자 공개 여부 (True 상태라면 일반 유저가 이 내전의 참가자를 조회할 수 없어요)"
				}
			)
		),
		channel: disnake.TextChannel = commands.Param(
			default=None,
			name=disnake.Localized(
				"alert_channel",
				data={
					disnake.Locale.ko: "알림_채널"
				}
			),
			description=disnake.Localized(
				"Custom game notification channel (sends participation button, all notifications!)",
				data={
					disnake.Locale.ko: "내전 알림 채널 (이 채널로 내전 참가 신청 버튼, 모든 내전 알림이 발송됩니다!)"
				}
			)
		)
	):
		await i.response.defer(ephemeral=True)
		roomId = createCustomGame(i.user.id, i.guild.id, name, gameType, open, open_user, channel.id if channel else None)
		await i.edit_original_message(
			embed=disnake.Embed(
				title="✅ 내전 생성 완료!",
				description=f"내전 코드: `{roomId}`\n내전 설정은 언제나 `/내전 설정 [내전 코드]`로 변경할 수 있어요!",
				color=0x00ff00
			))
	
	@customGame.sub_command(
		name=disnake.Localized(
			"search",
			data={
				disnake.Locale.ko: "검색"
			}
		),
		description=disnake.Localized(
			"Search for a custom game.",
			data={
				disnake.Locale.ko: "내전을 검색해요."
			}
		)
	)
	async def searchCustom_slashCommand(
		self, i: disnake.CommandInteraction
	):
		pass

	async def customGameList_autocomplete(
		self, i: disnake.CommandInteraction, name: str
	):
		if name == "" or name == None:
			res = searchCustomGame(userId=i.user.id, end=0)
		else:
			res = searchCustomGame(name=name, end=0)
		result = []
		gameType = ["솔로", "듀오", "스쿼드", "코발트"]
		for x in res:
			result.append(
				disnake.OptionChoice(
					name=f"{x[1]} ({gameType[x[3]-1]})",
					value=x[0]
				)
			)
		return result

	@customGame.sub_command(
		name=disnake.Localized(
			"delete",
			data={
				disnake.Locale.ko: "삭제"
			}
		),
		description=disnake.Localized(
			"Delete a custom game.",
			data={
				disnake.Locale.ko: "내전을 삭제해요."
			}
		)
	)
	async def deleteCustom_slashCommand(
		self, i: disnake.CommandInteraction,
		roomId: int = commands.Param(
			name=disnake.Localized(
				"code",
				data={
					disnake.Locale.ko: "코드"
				}
			),
			description=disnake.Localized(
				"custom game room code",
				data={
					disnake.Locale.ko: "내전 코드"
				}
			),
			autocomplete=customGameList_autocomplete
		)
	):
		await i.response.defer(ephemeral=True)
		deleteCustomGame(roomId)
		await i.edit_original_message(
			embed=disnake.Embed(
				title="✅ 내전 삭제 완료!",
				description=f"내전 코드: `{roomId}`",
				color=0x00ff00
			))
		
	@customGame.sub_command(
		name=disnake.Localized(
			"list",
			data={
				disnake.Locale.ko: "목록"
			}
		),
		description=disnake.Localized(
			"List all open custom games.",
			data={
				disnake.Locale.ko: "공개된 내전 목록을 나열해요."
			}
		)
	)
	async def listCustom_slashCommand(
		self, i: disnake.CommandInteraction
	):
		pass

	@customGame.sub_command(
		name=disnake.Localized(
			"join",
			data={
				disnake.Locale.ko: "참가"
			}
		),
		description=disnake.Localized(
			"Join a custom game.",
			data={
				disnake.Locale.ko: "내전에 참가해요."
			}
		)
	)
	async def joinCustom_slashCommand(
		self, i: disnake.CommandInteraction,
		roomId : int = commands.Param(
			name=disnake.Localized(
				"code",
				data={
					disnake.Locale.ko: "코드"
				}
			),
			description=disnake.Localized(
				"custom game code",
				data={
					disnake.Locale.ko: "내전 코드"
				}
			)
		),
		player : str = commands.Param(
			name=disnake.Localized(
				"nickname",
				data={
					disnake.Locale.ko: "닉네임"
				}
			),
			description=disnake.Localized(
				"Eternal Return nickname",
				data={
					disnake.Locale.ko: "이터널 리턴 닉네임"
				}
			)
		)
	):
		await i.response.defer(ephemeral=True)
		userId = await getUserId(player); userLvl = await getUserLevel(userId)
		embed = disnake.Embed(
			title="본인 확인", color=0xff0000,
			description=f"정말 **{player}**(Lv.{userLvl}) 님이 맞으신가요?\n\n**__자신이 아닌 계정, 부계정 등__** 올바르게 등록하지 않은 경우\n**__이하봇 운영정책에 의거해 이용이 제한될 수 있습니다!__**",
		)
		await i.edit_original_message(embed=embed, view=CustomGame_JoinCheck(userId=userId,roomId=roomId))

def setup(bot: commands.Bot):
	bot.add_cog(CustomGame(bot))