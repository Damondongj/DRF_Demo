import time
import wget
import requests
from lxml import etree

from selenium import webdriver

driver = webdriver.Chrome()

driver.get("http://www.51hei.com/bbs/")

username_input = driver.find_element_by_xpath('//*[@id="ls_username"]')
username_input.send_keys("1043411186@")

password_input = driver.find_element_by_xpath('//*[@id="ls_password"]')
password_input.send_keys("LiuJie@123")

login_button = driver.find_element_by_xpath('//*[@id="lsform"]/div/div[1]/table/tbody/tr[2]/td[3]/button')
login_button.click()
time.sleep(3)

cookies = driver.get_cookies()
session = requests.Session()
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

# driver.execute_script("window.open('http://www.51hei.com/bbs/forum.php?mod=attachment&aid=Mjg4NDc2fDU2ZWNjOTk3fDE2ODE3ODA2OTR8MHwyMTYzODQ%3D')")
#
# handles = driver.window_handles
#
# driver.switch_to.window(handles[1])
