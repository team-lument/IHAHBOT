import plotly.graph_objects as go

# 데이터 (x: 날짜, y: 값)
x_data = ['10/25', '10/27', '10/29', '10/31', '11/2', '11/4', '11/6', '11/8', '11/10']
y_data = [900, 1100, 1150, 1200, 1300, 1000, 1443, 1390, 1100]

# 마커 색상 설정 (각각 다른 값에 대해 색상 변경)
colors = ['orange', 'orange', 'orange', 'orange', 'blue', 'orange', 'blue', 'blue', 'orange']

fig = go.Figure(data=go.Scatter(
    x=x_data, 
    y=y_data,
    mode='lines+markers',
    marker=dict(
        color=colors,   # 각 점에 색상 적용
        size=10,        # 마커 크기
        line=dict(width=2)  # 마커 테두리 설정
    ),
    line=dict(color='white', width=2)  # 선의 색상과 굵기 설정
))

fig.update_layout(
    paper_bgcolor='black',  # 배경 색상
    plot_bgcolor='black',   # 플롯 배경 색상
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='white'),  # x축 격자
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='white'),  # y축 격자
    title="Data Over Time",
    font=dict(color="white")  # 제목과 텍스트 색상
)

fig.show()