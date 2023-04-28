import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Image, Paragraph, Spacer, PageBreak, TableStyle

TEMP_PATH = r"E:\projects\djangoProject\DRF_Demo\media"


class PlotImage(object):
    def __int__(self):
        pass

    def plot(self):
        self.plotly_part2()
        self.plotly_part3()
        self.plotly_part4()
        self.plotly_part5()

    def plotly_part2(self):
        score = 85

        fig = go.Figure(go.Pie(
            values=[score, 100 - score],
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
            plot_bgcolor='#FFFFFF', width=500, height=380, margin=dict(t=80, b=50, l=50, r=50)
        )

        fig.add_annotation(x=0.5, y=0.5, text=f"{score}", font=dict(family='Arial', size=36, color='#E83F2F'),
                           showarrow=False)

        fig.add_annotation(x=0.5, y=0.2, text="分数", font=dict(family='Arial', size=32, color='#E83F2F'),
                           showarrow=False)

        fig.write_image(TEMP_PATH + "\\" + 'plotly_2.png')

    def plotly_part3(self):
        plot_data = [{'question_type': '反射天线', 'number_of_selected': 5},
                     {'question_type': '喇叭天线', 'number_of_selected': 20},
                     {'question_type': '线天线', 'number_of_selected': 10},
                     {'question_type': '阵列天线', 'number_of_selected': 10},
                     {'question_type': '面天线', 'number_of_selected': 15}]
        df = pd.DataFrame(plot_data)

        total = df['number_of_selected'].sum()
        df['percentage'] = df['number_of_selected'] / total

        fig = px.pie(df, values='percentage', names='question_type',
                     labels={'percentage': '占比', 'question_type': '类型'})

        fig.update_layout(
            margin=dict(l=50, r=50, t=50, b=50),  # 设置图表周围的边距
            legend=dict(x=-0.2, y=0.5, orientation='v'),  # 设置图例的位置和方向
            width=500, height=380
        )

        fig.update_traces(textposition='outside', textinfo='percent+label', textfont_size=12,
                          insidetextorientation='radial')

        fig.write_image(TEMP_PATH + "\\" + "\\" + "plotly_3.png")

    def plotly_part4(self):
        data = {'Method': ['Method 1', 'Method 2', 'Method 3', 'Method 4', 'Method 5', 'Method 6'],
                'Accuracy': [0.85, 0.92, 0.78, 0.34, 0.78, 0.34]}
        df = pd.DataFrame(data)

        colors = px.colors.qualitative.Plotly[:len(df)]

        fig = px.bar(df, x='Method', y='Accuracy', text=df['Accuracy'].apply(lambda x: f'{x:.2%}'), color=colors)
        fig.update_traces(textposition='auto')
        fig.update_layout(
            width=500, height=380, title='能力图谱分析', xaxis_title='', yaxis_title='准确率', showlegend=False)
        fig.write_image(TEMP_PATH + "\\" + 'plotly_4.png')

    def plotly_part5(self):
        datas = [
            {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA',
             'question_type': '反射天线',
             'number_of_selected': 5},
            {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA',
             'question_type': '喇叭天线',
             'number_of_selected': 20},
            {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA',
             'question_type': '线天线',
             'number_of_selected': 10},
            {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA',
             'question_type': '阵列天线',
             'number_of_selected': 10},
            {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA',
             'question_type': '面天线',
             'number_of_selected': 15},
            {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA',
             'question_type': '面天线',
             'number_of_selected': 15},
            {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA',
             'question_type': '面天线',
             'number_of_selected': 15},
            {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA',
             'question_type': '面天线',
             'number_of_selected': 15},
            {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA',
             'question_type': '面天线',
             'number_of_selected': 15},
            {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA',
             'question_type': '面天线',
             'number_of_selected': 15},
            {'paper_type': '天线类EDA', 'paper_type_1': '天线类EDA', 'paper_type_2': '天线类EDA',
             'question_type': '面天线',
             'number_of_selected': 15}
        ]

        titles = list(datas[0].keys())
        values = [[data[title] for data in datas] for title in titles]

        table = go.Table(
            header=dict(values=titles),
            cells=dict(values=values)
        )

        fig = go.Figure(data=[table])
        fig.update_layout(
            margin=dict(t=20, b=0),
        )

        fig.write_image(TEMP_PATH + "\\" + 'plotly_5.png', format='png')


def generate():
    """
        generate pdf
    """
    plot = PlotImage()
    plot.plot()

    # 定义常量
    TITLE = "EDA比测验证报告"
    TITLE_FONT = "Microsoft YaHei"
    TABLE_FONT = "SimSun"
    FONTSIZE_LG = 16
    FONTSIZE_SM = 12
    MARGIN = 0.5 * inch

    pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttc'))
    pdfmetrics.registerFont(TTFont('Microsoft YaHei', 'msyh.ttc'))

    file_path = TEMP_PATH + "\\" + "report.pdf"
    if os.path.exists(file_path):
        os.remove(file_path)

    # 创建PDF文档
    doc = SimpleDocTemplate(file_path, pagesize=letter,
                            rightMargin=MARGIN, leftMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN)
    elements = []

    # 添加标题
    title_style = ParagraphStyle(name='title_style', fontName=TITLE_FONT, fontSize=FONTSIZE_LG, fontWeight='bold',
                                 alignment=TA_CENTER)
    elements.append(Paragraph(TITLE, title_style))
    elements.append(Spacer(1, 0.5 * inch))

    # 1、用户基本信息
    section1_style = ParagraphStyle(name='section_style', fontName=TITLE_FONT, fontSize=FONTSIZE_SM, fontWeight='bold',
                                    textColor=colors.black)
    elements.append(Paragraph("1、用户基本信息", section1_style))
    elements.append(Spacer(1, 0.2 * inch))

    label_style = ParagraphStyle(name='label_style', fontName=TABLE_FONT, fontSize=10)
    para_style = ParagraphStyle(name='para_style', fontName=TABLE_FONT, fontSize=10, leading=16)
    data = [
        [Paragraph("被测EDA名称：", label_style), Paragraph("星火技术", para_style)],
        [Paragraph("被测EDA简介：", label_style), Paragraph("这是CST", para_style)]
    ]

    table = Table(data, colWidths=[90, 320])
    table_style = TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    # 2、考试成绩
    section2_style = ParagraphStyle(name='section_style', fontName=TITLE_FONT, fontSize=FONTSIZE_SM)
    elements.append(Paragraph("2、考试成绩", section2_style))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Image(TEMP_PATH + "\\" + "plotly_2.png", width=4 * inch, height=3 * inch))

    # 3、试卷内容1
    section3_style = ParagraphStyle(name='section_style', fontName=TITLE_FONT, fontSize=FONTSIZE_SM)
    elements.append(Paragraph("3、试卷内容", section3_style))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(
        Image(TEMP_PATH + "\\" + "plotly_3.png", width=4.4 * inch, height=3.3 * inch))

    elements.append(PageBreak())

    # 添加试卷内容2
    section4_style = ParagraphStyle(name='section_style', fontName=TITLE_FONT, fontSize=FONTSIZE_SM)
    elements.append(Paragraph("4、试卷内容", section4_style))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Image(TEMP_PATH + "\\" + "plotly_4.png", width=6 * inch, height=4.5 * inch))
    elements.append(Spacer(1, 0.3 * inch))

    # 添加答题详情
    section5_style = ParagraphStyle(name='section_style', fontName=TITLE_FONT, fontSize=FONTSIZE_SM)
    elements.append(Paragraph("5、答题详情", section5_style))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Image(TEMP_PATH + "\\" + "plotly_5.png", width=6 * inch, height=4.5 * inch))

    doc.build(elements)

    return file_path


if __name__ == '__main__':
    generate()
