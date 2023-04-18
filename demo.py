import requests
from lxml import etree
from retrying import retry
from bs4 import BeautifulSoup
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


def parse_outer():
    inner = {}
    max_page = 10
    base_url = "http://www.51hei.com/bbs/search.php?mod=forum&searchid=467&orderby=lastpost&ascdesc=desc&searchsubmit=yes&page="
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
                # if href != "http://www.51hei.com/bbs/dpj-216384-1.html":
                inner[title] = href
    return inner
 

def parser_inner(title_url):
    for title, url in title_url.items():
        html = fetch(url)
        html = etree.HTML(html)
        print(url)
        try:
            postlist_div = html.xpath('//*[@id="postlist"]')[0]
            first_div = postlist_div.xpath('./div')[0]
            attnm_div = first_div.find('.//p[@class="attnm"]')
            print(attnm_div)
            print(first_div.get("id"))
        except Exception:
            print("HTML error!!!")
            continue
    return title_url


def main():
    title_url = parse_outer()
    title_url = parser_inner(title_url)
    # print(title_url)


if __name__ == '__main__':
    main()
