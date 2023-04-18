import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
from retrying import retry
from fake_headers import Headers

BASE_URL = "http://www.51hei.com"


@retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
def fetch(url, **kwargs):
    try:
        headers = Headers(headers=True).generate()
        kwargs.setdefault("verify", False)
        kwargs.setdefault("headers", headers)
        response = requests.get(url, **kwargs)
        if response.status_code == 200:
            return response.text
    except (requests.ConnectionError, requests.ReadTimeout):
        return


def parser_outer(url):
    html = fetch(url)
    # html = etree.HTML(html)
    html = etree.HTML(html)
    pages = html.xpath('//*[@id="ct"]/div/div/div[3]/div/label/span/text()')[0]
    import re
    max_page = int(re.findall(r"\d+", pages)[0])
    print(max_page)


def main():
    parser_outer(
        url="http://www.51hei.com/bbs/search.php?mod=forum&searchid=1557&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw=%D4%AD%C0%ED%CD%BC+PCB")


if __name__ == '__main__':
    main()
