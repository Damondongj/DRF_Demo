import plotly.graph_objs as go

data = [
    {'paper_type': '天线类EDA', 'question_type': '反射天线', 'number_of_selected': 5},
    {'paper_type': '天线类EDA', 'question_type': '喇叭天线', 'number_of_selected': 20},
    {'paper_type': '天线类EDA', 'question_type': '线天线', 'number_of_selected': 10},
    {'paper_type': '天线类EDA', 'question_type': '阵列天线', 'number_of_selected': 10},
    {'paper_type': '天线类EDA', 'question_type': '面天线', 'number_of_selected': 15}
]

# 创建表格
fig = go.Figure(data=[go.Table(
    header=dict(values=['Paper Type', 'Question Type', 'Number of Selected'],
                fill_color='#CCCCCC',
                align='center'),
    cells=dict(values=[[d['paper_type'] for d in data],
                       [d['question_type'] for d in data],
                       [d['number_of_selected'] for d in data]],
               fill_color='#F5F5F5',
               align='center'))
])

# 设置布局
fig.update_layout(width=500, height=300, margin=dict(l=50, r=50, t=50, b=50))

# 保存图像
fig.write_image('table.png', width=500, height=300)
