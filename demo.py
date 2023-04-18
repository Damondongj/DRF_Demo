import os
import wget
import requests
from lxml import etree
from retrying import retry
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_headers import Headers

BASE_URL = "http://www.51hei.com"


def get_cookies():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)

    username_input = driver.find_element_by_xpath('//*[@id="ls_username"]')
    username_input.send_keys("1043411186@")

    password_input = driver.find_element_by_xpath('//*[@id="ls_password"]')
    password_input.send_keys("LiuJie@123")

    login_button = driver.find_element_by_xpath('//*[@id="lsform"]/div/div[1]/table/tbody/tr[2]/td[3]/button')
    login_button.click()
    return driver.get_cookies()


@retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
def fetch(session, url):
    try:
        headers = Headers(headers=True).generate()
        session.headers.update(headers)
        response = session.get(url)
        if response.status_code == 200:
            return response.text
    except (requests.ConnectionError, requests.ReadTimeout):
        return


def download_zip(session, title_url):
    os.mkdir("./pcb")
    for title, urls in title_url.items():
        location = f"./pcb/{title}"
        os.makedirs(location)
        for url in urls:
            html = fetch(session, url)
            html = etree.HTML(html)
            href = html.xpath('//*[@id="messagetext"]/p[2]/a/@href')
            wget.download(href, location)


def parse_outer():
    inner = {}
    max_page = 10

    base_url = "http://www.51hei.com/bbs/search.php?mod=forum&searchid=384&orderby=lastpost&ascdesc=desc&searchsubmit=yes&page="
    for page in range(1, max_page + 1):
        url = base_url + str(page)
        html = fetch(url)
        soup = BeautifulSoup(html, "html.parser")
        lis = soup.select("#threadlist > ul > li")
        for li in lis:
            child = li.findChildren("a")[0]
            title = '_'.join([child.text] + [strong.text for strong in child.findAll("strong")])
            href = BASE_URL + child["href"]
            if title.__contains__("PCB") or title.__contains__("pcb") or title.__contains__(
                    "Pcb") or title.__contains__("原理图"):
                inner[title] = href
    return inner


def parser_inner(title_url):
    for title, url in title_url.items():
        html = fetch(url)
        # html = etree.HTML(html)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            # postlist_div = html.xpath('//*[@id="postlist"]')[0]
            # first_div = postlist_div.xpath('./div')[0]
            # download_url = first_div.xpath('.//p[@class="attnm"]/a/@href')
            download_url = []
            for a in soup.find_all('a', href=True):
                if any(ext in a.text for ext in ['.zip', '.rar', '.doc', '.7z']):
                    download_url.append(a['href'])
            if len(download_url) != 0:
                title_url[title] = download_url
                print(download_url)
        except Exception:
            print("HTML error!!!")
    return title_url


def main():
    session = requests.Session()
    cookies = get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    title_url = parse_outer()
    title_url = parser_inner(title_url)
    download_zip(session, title_url)


if __name__ == '__main__':
    main()
