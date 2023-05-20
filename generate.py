import os
import pandas as pd
from pathlib import Path
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

TEMP_PATH = str(Path.cwd()) + "\\media\\temp_file"
if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)


class PlotImage(object):
    def __init__(self, data):
        self.data = self.pre_process(data)

    def pre_process(self, data):
        df = pd.DataFrame(data["test_questions"])

        grouped = df.groupby("total_type").agg({"score": "sum", "got_score": "sum"})
        counts = df["total_type"].value_counts()
        grouped["counts"] = counts

        data["sum_result"] = grouped.reset_index()
        data["score"] = df["got_score"].sum()
        data["total_score"] = df["score"].sum()

        return data

    def plot(self):
        self.plotly_part2()
        self.plotly_part3()
        self.plotly_part4()

    def plotly_part2(self):
        score = self.data["score"]
        total_score = self.data["total_score"]

        fig = go.Figure(go.Pie(
            values=[score, total_score - score],
            hole=0.95,
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
            plot_bgcolor='#FFFFFF', width=500, height=380, margin=dict(t=80, b=40, l=0, r=0)
        )

        fig.add_annotation(x=0.5, y=1.10, text=f"试卷总分： {total_score}",
                           font=dict(family='Arial', size=16, color='#808080'),
                           showarrow=False)

        fig.add_annotation(x=0.5, y=0.5, text=f"{score}", font=dict(family='Arial', size=36, color='#E83F2F'),
                           showarrow=False)

        fig.add_annotation(x=0.5, y=0.2, text="分数", font=dict(family='Arial', size=32, color='#E83F2F'),
                           showarrow=False)

        fig.write_image(TEMP_PATH + "\\" + 'plotly_2.png', scale=10)

    def plotly_part3(self):
        df = self.data["sum_result"].loc[:, ["total_type", "counts"]]

        total = df['counts'].sum()
        df['percentage'] = df['counts'] / total

        fig = px.pie(df, values='percentage', names='total_type',
                     labels={'percentage': '占比', 'type': '类型'})

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(x=-0.4, y=1.5, orientation='v'),
            width=500, height=380
        )

        fig.update_traces(textposition='outside', textinfo='percent+label', textfont_size=12,
                          insidetextorientation='radial')

        fig.write_image(TEMP_PATH + "\\" + "plotly_3.png", scale=10)

    def plotly_part4(self):
        df = self.data["sum_result"].loc[:, ["total_type", "score", "got_score"]]
        df["Accuracy"] = df["got_score"] / df["score"]
        df = df.loc[:, ["total_type", "Accuracy"]]

        colors = px.colors.qualitative.Plotly[:len(df)]

        fig = px.bar(df, x='total_type', y='Accuracy', text=df['Accuracy'].apply(lambda x: f'{x:.2%}'), color=colors)
        fig.update_traces(textposition='auto')
        fig.update_layout(
            width=600, height=450, title='能力图谱分析', xaxis_title='', yaxis_title='准确率', showlegend=False,
            margin=dict(l=60, r=60, t=80, b=0))
        fig.write_image(TEMP_PATH + "\\" + 'plotly_4.png', scale=10)


def calculate_padding(text, font_name, font_size, width):
    text_width = pdfmetrics.stringWidth(text, font_name, font_size)
    padding = (width - text_width) / 2
    return padding


def generate_pictures(data):
    plot = PlotImage(data)
    plot.plot()


def generate_pdf(data):
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

    label_style = ParagraphStyle(name='label_style', fontName=TABLE_FONT, fontSize=10)
    para_style = ParagraphStyle(name='para_style', fontName=TABLE_FONT, fontSize=10, leading=16)

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

    table_data = [
        [Paragraph("被测EDA名称: ", label_style), Paragraph(f'{data["test_eda_name"]}', para_style)],
        [Paragraph("被测EDA简介: ", label_style), Paragraph(f'{data["test_eda_desc"]}', para_style)]
    ]

    font_name = "Helvetica"
    font_size = 12
    first_padding = calculate_padding(data["test_eda_name"], font_name, font_size, 320)
    second_padding = calculate_padding(data["test_eda_desc"], font_name, font_size, 320)

    styles = [
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), font_name),
        ('FONTSIZE', (0, 1), (-1, -1), font_size),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (1, 0), (1, 0), first_padding),
        ('RIGHTPADDING', (1, 0), (1, 0), first_padding),
        ('LEFTPADDING', (1, 1), (1, 1), second_padding),
        ('RIGHTPADDING', (1, 1), (1, 1), second_padding),
    ]

    if pdfmetrics.stringWidth(data["test_eda_desc"], font_name, font_size) > 320:
        styles = styles[:-2]
    table_style = TableStyle(styles)
    table = Table(table_data, colWidths=[73, 320])
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
        Image(TEMP_PATH + "\\" + "plotly_3.png", width=5 * inch, height=3.9 * inch))
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
    elements.append(Spacer(1, 0.3 * inch))
    test_questions = data["test_questions"]
    for item in test_questions:
        item["类型"] = item.pop("total_type")  # 将 "total_type" 替换为 "类型"
        item["分值"] = item.pop("score")  # 将 "score" 替换为 "得分"
        item["得分"] = item.pop("got_score")
        item["产品类型"] = item.pop("product_type")
        item["测试功能"] = item.pop("test_function")

    font_name = 'Helvetica-Bold'
    detail_question_styles = [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (-1, -1), (-1, -1), font_name),
        ('FONTSIZE', (-1, -1), (-1, -1), font_size),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]

    colWidths = [35, 100, 35, 35, 140, 160]
    detail_table_data = []
    column_list = []
    for index, column in enumerate(["序号"] + list(test_questions[0].keys())):
        column_list.append(Paragraph(column, label_style))
        column_padding = calculate_padding(column, font_name, font_size, colWidths[index])
        detail_question_styles.append(('LEFTPADDING', (index, 0), (index, 0), column_padding))

    detail_table_data.append(column_list)

    for index, question in enumerate(test_questions):
        paragraphList = [Paragraph(f"{index + 1}", para_style)]
        first_index_padding = calculate_padding(str(index + 1), font_name, font_size, colWidths[0])
        detail_question_styles.append(('RIGHTPADDING', (0, index + 1), (0, index + 1), first_index_padding))
        for inner_index, value in enumerate(list(question.values())):
            paragraphList.append(Paragraph(f"{value}", para_style))
            padding = calculate_padding(str(value), font_name, font_size, colWidths[inner_index + 1])
            detail_question_styles.append(
                ('LEFTPADDING', (inner_index + 1, index + 1), (inner_index + 1, index + 1), padding))

        detail_table_data.append(paragraphList)
    detail_question_table_style = TableStyle(detail_question_styles)

    table = Table(detail_table_data, colWidths=colWidths)
    table.setStyle(detail_question_table_style)
    elements.append(table)

    doc.build(elements)

    return file_path


def generate(data):
    """
        generate pdf
    """
    generate_pictures(data)
    file_path = generate_pdf(data)
    return file_path


if __name__ == '__main__':
    data = {
        "test_eda_name": "aaa",
        "test_eda_desc": "fsdfsadfsdh",
        "test_questions": [
            {"total_type": "aaaaa", "score": 10, "got_score": 8, "product_type": "阵列天线",
             "test_function": "版图设计版图设计版图设计版图设计"},
            {"total_type": "aaaaa", "score": 20, "got_score": 12, "product_type": "阵列天线",
             "test_function": "版图设计"},
            {"total_type": "bbbbb", "score": 10, "got_score": 8, "product_type": "阵列天线",
             "test_function": "版图设计"},
            {"total_type": "ccccc", "score": 10, "got_score": 7, "product_type": "阵列天线",
             "test_function": "版图设计"},
            {"total_type": "ddddd", "score": 5, "got_score": 4, "product_type": "阵列天线",
             "test_function": "版图设计"},
            {"total_type": "ddddd", "score": 5, "got_score": 3, "product_type": "阵列天线",
             "test_function": "版图设计"},
            {"total_type": "eeeee", "score": 20, "got_score": 20, "product_type": "阵列天线",
             "test_function": "版图设计"},
            {"total_type": "fffff", "score": 10, "got_score": 8, "product_type": "阵列天线",
             "test_function": "版图设计"},
            {"total_type": "ggggg", "score": 10, "got_score": 9, "product_type": "阵列天线",
             "test_function": "版图设计"},
            {"total_type": "fffff", "score": 10, "got_score": 8, "product_type": "阵列天线",
             "test_function": "版图设计"},
            {"total_type": "ggggg", "score": 10, "got_score": 9, "product_type": "阵列天线",
             "test_function": "版图设计"},
            {"total_type": "aaaaa", "score": 10, "got_score": 8, "product_type": "阵列天线",
             "test_function": "版图设计"},
            {"total_type": "aaaaa", "score": 20, "got_score": 12, "product_type": "阵列天线",
             "test_function": "版图设计"},
        ],
    }
    path = generate(data)
    print(path)
