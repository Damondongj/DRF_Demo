import plotly.graph_objs as go

datas = [
    {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA', 'question_type': '反射天线',
     'number_of_selected': 5},
    {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA', 'question_type': '喇叭天线',
     'number_of_selected': 20},
    {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA', 'question_type': '线天线',
     'number_of_selected': 10},
    {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA', 'question_type': '阵列天线',
     'number_of_selected': 10},
    {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA', 'question_type': '面天线',
     'number_of_selected': 15}
    ,
    {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA', 'question_type': '面天线',
     'number_of_selected': 15}
    ,
    {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA', 'question_type': '面天线',
     'number_of_selected': 15}
    ,
    {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA', 'question_type': '面天线',
     'number_of_selected': 15}
    ,
    {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA', 'question_type': '面天线',
     'number_of_selected': 15}
    ,
    {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA', 'question_type': '面天线',
     'number_of_selected': 15}
    ,
    {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA', 'question_type': '面天线',
     'number_of_selected': 15}

]

titles = list(datas[0].keys())

values = [[data[title] for data in datas] for title in titles]

table = go.Table(
    header=dict(values=titles),

    cells=dict(values=values)
)

fig = go.Figure(data=[table])
# fig.update_layout(
#     width=500, height=380
# )

fig.write_image('plotly_5.png', format='png')
