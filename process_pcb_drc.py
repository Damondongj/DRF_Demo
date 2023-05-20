import json
from pathlib import Path
from lxml import etree


def read_html(file_path):
    with open(file_path, "r") as f:
        data = f.read()
    html = etree.HTML(data)
    return html


def process_prb_drc(file_path):
    result = {
        "model_name": Path(file_path).stem,
        "PCB_DRC":
            {
                "Clearance Constraint": 0,
                "Short-Circuit Constraint": 0,
                "Un-Routed Net Constraint": 0,
                "Modified Polygon": 0,
                "Width Constraint": 0,
                "Routing Via": 0,
                "Minimum Solder Mask Sliver": 0,
                "Silk To Solder Mask": 0,
                "Net Antennae": 0,
                "Component Clearance Constraint": 0,
                "Height Constraint": 0
            },
    }
    html = read_html(file_path)
    trs = html.xpath('/html/body/table[3]/tr')
    for tr in trs[1: -1]:
        key = tr.xpath("./td/a/text()")[0].split("(")[0].rstrip()
        content = int(tr.xpath("./td/text()")[0])
        result["PCB_DRC"][key] = content

    print(result)
    return json.dumps(result)


if __name__ == '__main__':
    file_path = r"C:\Users\star\Desktop\Answer_PCB\Answer_PCB\39_Design Rule Check - Radar1_PCB_Solder1.html"
    result = process_prb_drc(file_path)
