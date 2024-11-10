import disnake
def makeErrorEmbed(desc:str="내부 오류가 발생했어요."): return disnake.Embed(title=":warning: 오류!", description=desc, color=0xFF0000)

def helpEmbed():
	embed = disnake.Embed(color=0xabcdef, title="👋 안녕하세요! 이하봇이에요.")
	embed.add_field(name="/핑", value=f"네트워크 지연 상태와 API 서버 상태를 확인해요.", inline=False)
	embed.add_field(name="/전적 [이터널 리턴 유저명 또는 초성으로 검색]", value=f"이터널 리턴 유저 전적 및 대전 목록을 보여줘요. (초성 검색 가능)", inline=False)
	embed.add_field(name="/로테이션", value=f"이터널 리턴 무료 캐릭터 로테이션을 보여줘요.", inline=False)
	embed.add_field(name="/루트 [루트 이름 또는 루트 ID]", value=f"루트 정보를 보여줘요.\n루트 이름으로 작성할 경우 루트를 검색해요.", inline=False)
	embed.add_field(name="/동접", value=f"현재 이터널 리턴 동접을 보여줘요.", inline=False)
	embed.add_field(name="/소식", value=f"이터널 리턴 공식 홈페이지의 공지를 보여줘요.", inline=False)
	embed.add_field(name="/시즌", value="다음 시즌까지 남은 시간을 알려줘요.", inline=False)
	embed.add_field(name="/이터컷 (시즌명) (솔로/듀오/스쿼드)", value="해당 시즌과 해당 모드의 이터니티 컷을 확인해요.\n시즌을 입력하지 않으면 현재 시즌, 모드를 입력하지 않으면 솔로 또는 스쿼드를 보여줘요.", inline=False)
	embed.set_footer(text="다음 페이지에 이어져요!")
	return embed

developer = """**이터널 리턴 닉네임**: [샨티](https://aya.gg/ko/players/샨티)
**X** (트위터): [@rai_ny__inside](https://x.com/rai_ny__inside), **치지직**: [라이니](https://chzzk.naver.com/75478606be9ae1aa3b748fbe756ffdb6)
**서포트 서버**: https://discord.gg/cf3D2HCzEh"""

def helpEmbed2():
	embed = disnake.Embed(color=0xabcdef)
	embed.add_field(name="/데이터베이스 아이템 [아이템]", value="이하봇 DB에서 아이템을 검색해요.", inline=False)
	embed.add_field(name="/데이터베이스 캐릭터 [캐릭터]", value="이하봇 DB에서 캐릭터를 검색해요.", inline=False)
	embed.add_field(name="/데이터베이스 스킨 [스킨]", value="이하봇 DB에서 스킨을 검색해요.", inline=False)
	embed.add_field(name="/환경변수 설정 [키] [값]", value=f"환경 변수를 등록해요.")
	embed.add_field(name="/환경변수 확인", value=f"환경 변수를 가져와요.")
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