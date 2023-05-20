import json
from pathlib import Path


# 原理图
def territory_drc(file_path, html_path):
    def parse_line(line):
        device_name, error = line.split("(")
        error = error.split(")")[0]
        if error.__contains__(":"):
            error = error.split(":")[0]
        return device_name.strip(), error

    result = {
        "model_name": Path(file_path).stem,
        "SCH_DRC": {
            "Missing Pin Name": [],
            "Duplicate Pin Number": [],
            "No Description": [],
            "No Footprint": [],
            "Missing Pin Number": [],
            "Missing-Default Designator": 0,  # 元件位号为填写需要解析17_Radar1_SCH_MDD1.html Error个数
            "Missing Pin Number In Sequence": []
        }
    }

    # [parse_line(line) for i, line in enumerate(f) if i >= 4]
    with open(file_path, "r") as f:  # 跳过第一行
        first_line = next(f)
        for i, line in enumerate(f):
            if i >= 4:
                device_name, error = parse_line(line)
                result["SCH_DRC"][error] = device_name

    with open(html_path, "r") as f:
        data = f.read()
    counts = data.count("[Error]")
    result["SCH_DRC"]["Missing-Default Designator"] = counts
    print(result)
    return json.dumps(result)


if __name__ == '__main__':
    result = territory_drc(r"C:\Users\star\Desktop\Answer_PCB\Answer_PCB\19_Radar1_SCH_MMPS1.ERR",
                           r"C:\Users\star\Desktop\Answer_PCB\Answer_PCB\17_Radar1_SCH_MDD1.html")
    with open("aaa.json", "w") as f:
        f.write(result)
