import plotly.graph_objects as go

# 准备数据
score = 85

# 绘制环形图
fig = go.Figure(go.Pie(
    values=[score, 100-score],
    hole=0.85,
    rotation=90,
    direction="clockwise",
    showlegend=False,
    marker=dict(colors=["#E83F2F", "#E7EFF0"], line=dict(color='#E7EFF0', width=1)),
    textinfo='none',
))

fig.update_layout(
    title={
        'text': '南京星火技术有限公司',
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(family='Arial', size=20, color='#333'),
    },
    plot_bgcolor='#FFFFFF',
    width=500,
    height=380,
    margin=dict(t=80, b=50, l=50, r=50),
)


# 添加中心文本
fig.add_annotation(
    x=0.5,
    y=0.5,
    text=f"{score}%",
    font=dict(family='Arial', size=36, color='#E83F2F'),
    showarrow=False,
)

fig.add_annotation(
    x=0.5,
    y=0.2,
    text="得分",
    font=dict(family='Arial', size=16, color='#E83F2F'),
    showarrow=False,
)

# 保存图像
fig.write_image('score_pie.png')
