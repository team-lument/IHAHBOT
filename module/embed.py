import disnake

from module.database import WeaponEmoji, getArea, getCharacterName, getCharacterWeapon
from module.route import generateSkillTree
def makeErrorEmbed(desc:str="내부 오류가 발생했어요."): return disnake.Embed(title=":warning: 오류!", description=desc, color=0xFF0000)

def helpEmbed():
	embed = disnake.Embed(color=0xabcdef, title="👋 안녕하세요! 이하봇이에요.")
	embed.add_field(name="/핑", value=f"네트워크 지연 상태와 API 서버 상태를 확인해요.", inline=False)
	embed.add_field(name="/전적 [이터널 리턴 유저명 또는 초성으로 검색]", value=f"이터널 리턴 유저 전적 및 대전 목록을 보여줘요. (초성 검색 가능)", inline=False)
	embed.add_field(name="/로테이션", value=f"이터널 리턴 무료 캐릭터 로테이션을 보여줘요.", inline=False)
	# embed.add_field(name="🛠️ /루트 [루트 이름 또는 루트 ID]", value=f"루트 정보를 보여줘요.\n루트 이름으로 작성할 경우 루트를 검색해요.", inline=False)
	embed.add_field(name="/동접", value=f"현재 이터널 리턴 동접을 보여줘요.", inline=False)
	# embed.add_field(name="🛠️ /소식", value=f"이터널 리턴 공식 홈페이지의 공지를 보여줘요.", inline=False)
	embed.add_field(name="/시즌", value="다음 시즌까지 남은 시간을 알려줘요.", inline=False)
	embed.add_field(name="/랭킹 RP", value="프리 시즌이 아닌 현재 시즌의 RP 랭킹을 불러와요.\n이터니티와 데미갓의 최저 RP도 함께 보여줘요.\n선택하면 해당 유저의 전적을 확인해요.", inline=False)
	embed.add_field(name="/랭킹 장인력 [캐릭터]", value="프리 시즌이 아닌 현재 시즌의 장인력 랭킹을 불러와요.\n선택하면 해당 유저의 전적을 확인해요.", inline=False)
	embed.set_footer(text="다음 페이지에 이어져요!")
	return embed

developer = """**이터널 리턴 닉네임**: [샨티](https://aya.gg/ko/players/샨티)
**X** (트위터): [@rai_ny__inside](https://x.com/rai_ny__inside), **치지직**: [라이니](https://chzzk.naver.com/75478606be9ae1aa3b748fbe756ffdb6)
**서포트 서버**: https://discord.gg/cf3D2HCzEh"""

def helpEmbed2():
	embed = disnake.Embed(color=0xabcdef)
	embed.add_field(name="🛠️ /데이터베이스 아이템 [아이템]", value="이하봇 DB에서 아이템을 검색해요.", inline=False)
	embed.add_field(name="/데이터베이스 캐릭터 [캐릭터]", value="이하봇 DB에서 캐릭터를 검색해요.", inline=False)
	embed.add_field(name="/환경변수 설정 [키] [값]", value=f"환경 변수를 등록해요.")
	embed.add_field(name="🛠️ /환경변수 확인", value=f"환경 변수를 가져와요.")
	embed.add_field(name="개발자와 소통해요.", value=developer, inline=False)
	embed.set_footer(text="Made By rai_ny._.")
	return embed

def SpecialThanks():
	embed = disnake.Embed(color=0xabcdef, title="Credit / Special Thanks")
	embed.add_field(name="Main Developer", value="라이니 `@rai_ny._.`", inline=False)
	embed.add_field(name="Supporter", value=">>> 지빵 `@jippang`\n응애 `@whygamja`\n크로니아 `@croniakr`", inline=False)
	embed.add_field(name="Development Help", value="- KOZ39 `@koz39`\n> Reports various errors.\n> Help for making `/ccu` command", inline=False)
	embed.add_field(name="Service Data", value="> [Aya.gg](https://aya.gg)", inline=False)
	return embed

def routeEmbed(x: dict):
	embed = disnake.Embed(
		title=x['title']
	)
	tree = generateSkillTree(x['preferences']['skills'])
	[character, weapon] = getCharacterWeapon(x['characterWeaponId'])
	embed.add_field(name="실험체", value=f"{WeaponEmoji(weapon)} {getCharacterName(character)}")
	embed.add_field(name="제작자", value=x['playerName'])
	embed.add_field(name="좋아요", value=x['likes'])
	embed.add_field(name="스킬트리", value=f"**{' → '.join(tree[1])}**\n{' → '.join(tree[0])}", inline=False)
	embed.add_field(name="지역", value=' → '.join([getArea(a) for a in x['preferences']['areas']]))
	return embed