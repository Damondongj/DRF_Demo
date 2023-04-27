import json
import asyncio
from lxml import etree
from pathlib import Path


async def read_html(file_path):
    with open(file_path, "r") as f:
        data = f.read()
    html = etree.HTML(data)
    return html


async def process_inner(file_path):
    html = await read_html(file_path)
    trs = html.xpath("/html/body/font[1]/table[1]/tr[1]/td[2]/font[1]/table[1]/tr")
    result = {}
    for tr in trs:
        key = tr.xpath("./td[1]/font/b/text()")[0].strip()
        value = tr.xpath("./td[2]//font/text()")[0].strip()
        result[key] = value
    return result


async def process_html(file_path):
    html = await read_html(file_path)
    trs = html.xpath('/html/body/font/table/tr')
    result = {}
    for tr in trs[5:]:
        url = str(Path(file_path).parent) + "\\" + tr.xpath("./td[1]/font/a/@href")[0]
        content = tr.xpath("./td[1]/font/a/text()")[0]
        inner_content = await process_inner(url)
        result[content] = inner_content
    return json.dumps(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(process_html(r"C:\Users\star\Desktop\ProgramControl_1\ProgramControl_1.html"))
    print(result)
