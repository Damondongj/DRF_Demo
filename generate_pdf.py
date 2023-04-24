from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, Image, Paragraph, Spacer, PageBreak, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 定义常量
TITLE = "EDA比测验证报告"
TITLE_FONT = "Microsoft YaHei"
TABLE_FONT = "SimSun"
FONTSIZE_LG = 16
FONTSIZE_MD = 14
FONTSIZE_SM = 12
MARGIN = 0.5 * inch

pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttc'))
pdfmetrics.registerFont(TTFont('Microsoft YaHei', 'msyh.ttc'))

if os.path.exists("report.pdf"):
    os.remove("report.pdf")

# 创建PDF文档
doc = SimpleDocTemplate("report.pdf", pagesize=letter,
                        rightMargin=MARGIN, leftMargin=MARGIN,
                        topMargin=MARGIN, bottomMargin=MARGIN)
elements = []

# 添加标题
title_style = ParagraphStyle(name='title_style', fontName=TITLE_FONT, fontSize=FONTSIZE_LG, fontWeight='bold', alignment=TA_CENTER)
elements.append(Paragraph(TITLE, title_style))
elements.append(Spacer(1, 0.5 * inch))



# 1、用户基本信息
section1_style = ParagraphStyle(name='section_style', fontName=TITLE_FONT, fontSize=FONTSIZE_SM, fontWeight='bold', textColor=colors.black)
elements.append(Paragraph("1、用户基本信息", section1_style))
elements.append(Spacer(1, 0.2 * inch))

label_style = ParagraphStyle(name='label_style', fontName=TABLE_FONT, fontSize=10)
para_style = ParagraphStyle(name='para_style', fontName=TABLE_FONT, fontSize=10, leading=16)
data = [
    [Paragraph("被测EDA名称：", label_style), Paragraph("星火技术", para_style)],
    [Paragraph("被测EDA简介：", label_style), Paragraph("函数的覅解散分法氏囊佛奥死付军后该胡哥哥过过过过过过过扩军扩军扩女木吗1么么么么么么么么么 这种格式的发送到发士大夫发送到发三份发水电费第三方阿萨德发送到发三份阿萨德发士大夫", para_style)]
]

table = Table(data, colWidths=[90, 320])
table_style = TableStyle([
    ('ALIGN', (1,0), (1,-1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 12),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('TEXTCOLOR',(0,1),(-1,-1),colors.black),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 12),
    ('GRID', (0,0), (-1,-1), 1, colors.black)
])
table.setStyle(table_style)
elements.append(table)
elements.append(Spacer(1, 0.3 * inch))


# 2、考试成绩
section2_style = ParagraphStyle(name='section_style', fontName=TITLE_FONT, fontSize=FONTSIZE_SM)
elements.append(Paragraph("2、考试成绩", section2_style))
elements.append(Spacer(1, 0.1 * inch))
img = PILImage.open("score_pie.png")
width, height = img.size
aspect = height / float(width)
elements.append(Image("score_pie.png", width=4 * inch, height=3 * inch))
# elements.append(Spacer(1, 0.5 * inch))

# 3、试卷内容1
section3_style = ParagraphStyle(name='section_style', fontName=TITLE_FONT, fontSize=FONTSIZE_SM)
elements.append(Paragraph("3、试卷内容", section3_style))
elements.append(Spacer(1, 0.1 * inch))
img = PILImage.open("antenna_pie_chart.png")
width, height = img.size
aspect = height / float(width)
elements.append(Image("antenna_pie_chart.png", width=4.4 * inch, height=3.3 * inch))


elements.append(PageBreak())

# 添加试卷内容2
section4_style = ParagraphStyle(name='section_style', fontName=TITLE_FONT, fontSize=FONTSIZE_SM)
elements.append(Paragraph("4、试卷内容", section4_style))
elements.append(Spacer(1, 0.1 * inch))
img = PILImage.open("method_comparison.png")
width, height = img.size
aspect = height / float(width)
elements.append(Image("method_comparison.png", width=6 * inch, height=4.5 * inch))
elements.append(Spacer(1, 0.3 * inch))

# 添加答题详情
section5_style = ParagraphStyle(name='section_style', fontName=TITLE_FONT, fontSize=FONTSIZE_SM)
elements.append(Paragraph("5、答题详情", section5_style))
elements.append(Spacer(1, 0.1 * inch))
img = PILImage.open("score.png")
width, height = img.size
aspect = height / float(width)
elements.append(Image("score.png", width=6 * inch, height=(8 * aspect) * inch))

# 将所有元素添加到文档中并生成PDF文件
doc.build(elements)
