import requests
import time
import requests
import wget
from lxml import etree
from selenium import webdriver

# 登录请求的URL和数据
login_url = 'http://www.51hei.com/bbs/'
login_data = {
    'username': '1043411186@',
    'password': 'LiuJie@123',
}

# 创建Session对象
session = requests.Session()
response = session.post(login_url, data=login_data)

cookies = response.cookies.get_dict()

for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

html = session.get(
    "http://www.51hei.com/bbs/forum.php?mod=attachment&aid=Mjg4NDc2fDU2ZWNjOTk3fDE2ODE3ODA2OTR8MHwyMTYzODQ%3D").text
html = etree.HTML(html)
href = html.xpath('//*[@id="messagetext"]/p[2]/a/@href')
print(href)
import os

os.mkdir("./pcb")
os.makedirs("./pcb/T12焊台616电路原理图PCB文件 V6.0_原理图_PCB")
wget.download(href[0], "./pcb/T12焊台616电路原理图PCB文件 V6.0_原理图_PCB")
