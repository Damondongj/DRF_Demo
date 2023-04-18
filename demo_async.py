import os
import re
import wget
import shutil
import asyncio
import aiohttp
import requests
from lxml import etree
from retrying import retry
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_headers import Headers

BASE_URL = "http://www.51hei.com"
AUTO_URL = "http://www.51hei.com/bbs/"
SEARCH_URL = "http://www.51hei.com/bbs/search.php?mod=forum&searchid=384&orderby=lastpost&ascdesc=desc&searchsubmit=yes&page="


# def get_cookies():
#     driver = webdriver.Chrome()
#     driver.get(AUTO_URL)
#     username_input = driver.find_element_by_xpath('//*[@id="ls_username"]')
#     username_input.send_keys("1043411186@")
#     password_input = driver.find_element_by_xpath('//*[@id="ls_password"]')
#     password_input.send_keys("LiuJie@123")
#     login_button = driver.find_element_by_xpath('//*[@id="lsform"]/div/div[1]/table/tbody/tr[2]/td[3]/button')
#     login_button.click()
#     return driver.get_cookies()


def get_cookies():
    login_url = 'http://www.51hei.com/bbs/'
    login_data = {
        'username': '1043411186@',
        'password': 'LiuJie@123',
    }
    session = requests.Session()
    response = session.post(login_url, data=login_data)
    cookies = response.cookies.get_dict()
    return cookies


@retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return


async def download_zip(session, title_url):
    for title, urls in title_url.items():
        if len(urls) != 0:
            location = f"./pcb/{title}"
            os.makedirs(location)
            for url in urls:
                html = await fetch(session, url)
                html = etree.HTML(html)
                href = html.xpath('//*[@id="messagetext"]/p[2]/a/@href')
                await asyncio.run(wget.download(href, location))


async def parse_outer(session):
    inner = {}
    first_page = await fetch(session, SEARCH_URL + str(1))
    pages = etree.HTML(first_page).xpath('//*[@id="ct"]/div/div/div[3]/div/label/span/text()')[0]
    max_page = int(re.findall(r"\d+", pages)[0])
    for page in range(1, max_page + 1):
        url = SEARCH_URL + str(page)
        html = await fetch(session, url)
        soup = BeautifulSoup(html, "html.parser")
        lis = soup.select("#threadlist > ul > li")
        for li in lis:
            child = li.findChildren("a")[0]
            title = '_'.join([child.text] + [strong.text for strong in child.findAll("strong")])
            href = BASE_URL + child["href"]
            pattern = r'[\\/:*?"<>|]'
            title = re.sub(pattern, "_", title)
            if title.__contains__("PCB") or title.__contains__("pcb") or title.__contains__(
                    "Pcb") or title.__contains__("原理图"):
                inner[title] = href
    return inner


async def parser_inner(session, title_url):
    for title, url in title_url.items():
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            download_url = []
            for a in soup.find_all('a', href=True):
                if any(ext in a.text for ext in ['.zip', '.rar', '.doc', '.7z']):
                    download_url.append(a['href'])
            if len(download_url) != 0:
                title_url[title] = download_url
            print("aaa")
        except Exception:
            print("HTML error!!!")
    return title_url


async def main():
    if os.path.exists("./pcb"):
        shutil.rmtree("./pcb", ignore_errors=True)
    os.mkdir("./pcb")
    headers = Headers(headers=True).generate()
    async with aiohttp.ClientSession(headers=headers, cookies=get_cookies()) as session:
        title_url = await parse_outer(session)
        title_url = await parser_inner(session, title_url)
        await download_zip(session, title_url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
