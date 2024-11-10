import plotly.express as px
from pandas import DataFrame
import requests
from config import AYAGG_HEADER

def getTier(mmr: int, demigod: bool = False, eternity: bool = False):
	if eternity:		return "eternity"
	elif demigod: 		return "demigod"
	elif mmr == 0: 		return "unranked"
	elif mmr < 600: 	return "iron"
	elif mmr < 1400: 	return "bronze"
	elif mmr < 2400: 	return "silver"
	elif mmr < 3600: 	return "gold"
	elif mmr < 5000: 	return "platinum"
	elif mmr < 6400: 	return "diamond"
	elif mmr < 6800: 	return "meteorite"
	else:				return "mithril"

textColor = {
	"unranked": 	"hsl(0, 0%, 25%)",
	"iron": 		"hsl(0, 0%, 20%)",
	"bronze": 		"hsl(28, 60%, 15%)",
	"silver": 		"hsl(211, 26%, 15%)",
	"gold": 		"hsl(40, 66%, 15%)",
	"platinum": 	"hsl(151, 63%, 15%)",
	"diamond": 		"hsl(263, 25%, 15%)",
	"metheorite": 	"hsl(214, 70%, 15%)",
	"mithril": 		"hsl(191, 61%, 15%)",
	"demigod": 		"hsl(60, 100%, 15%)",
	"eternity": 	"hsl(340, 65%, 90%)",
}

markerColor = {
	"unranked": 	"rgb(240, 240, 240)",
    "iron": 		"rgb(229, 239, 255)",
    "bronze": 		"rgb(252, 149, 59)",
    "silver": 		"rgb(96, 127, 161)",
	"gold": 		"rgb(224, 184, 102)",
	"platinum": 	"rgb(122, 225, 175)",
	"diamond": 		"rgb(208, 196, 226)",
	"metheorite": 	"rgb(105, 159, 229)",
	"mithril": 		"rgb(130, 208, 225)",
	"demigod": 		"rgb(255, 255, 222)",
	"eternity": 	"rgb(160, 31, 74)"
}

# 샨티 님의 RP 변동 이력
url = "https://api.aya.gg/queues/by-player/3015759/history"
res = requests.get(url, headers=AYAGG_HEADER)
data : dict = res.json()['result']['3']
keys = list(data); df = []; tierColors = []; tierColors = []
for x in range(len(data)):
	df.append({ "date": "/".join([keys[x][i:i+2] for i in range(0, len(keys[x]), 2)])[3:], "rp": data[keys[x]]['end']})
	tier = getTier(data[keys[x]]['end'])
	tierColors.append(markerColor[tier])
fig = px.line(DataFrame.from_dict(df), x="date", y="rp", text="rp")
fig.update_traces(
	textposition="top center",
	textfont=dict(
		color=tierColors
	),
	line=dict(
		color='white',
		width=5
	),
	marker=dict(
		color=tierColors,
		colorscale='Viridis',
		cmin=0,
		cmax=50,
		size=15
	)
)

fig.update_xaxes(title=None, dtick=2)
fig.update_yaxes(title=None, dtick=100)
fig.update_layout(
	margin=dict(
		autoexpand=False,
		l=50,
		r=20,
		t=20,
		b=30
	),
	plot_bgcolor='rgba(0, 0, 0, 0)',
	paper_bgcolor='rgba(0, 0, 0, 0)',
	xaxis=dict(
		gridcolor='#575757',
		color='white',
		tickfont=dict(
			color='white'
		)
	),
	yaxis=dict(
		gridcolor='#575757',
		color='white',
		tickfont=dict(
			color='white'
		)
	)
)
fig.write_image("Match/mmr-history/3015759.png")