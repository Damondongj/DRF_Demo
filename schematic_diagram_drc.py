import json


# 原理图
def territory_drc(file_path):
    def parse_line(line):
        device_name, error = line.split("(")
        return {
            "device_name": device_name.strip(),
            "error": error.split(")")[0]
        }

    with open(file_path, "r") as f:  # 跳过第一行
        first_line = next(f)
        result = {
            "model_name": first_line.strip().split("\\")[-1],
            "errors": [parse_line(line) for i, line in enumerate(f) if i >= 4]
        }
    return json.dumps(result)


if __name__ == '__main__':
    print(territory_drc(r"C:\Users\star\Desktop\DRC\DRC\ProgramControll1_SCH_MPNu1.ERR"))
