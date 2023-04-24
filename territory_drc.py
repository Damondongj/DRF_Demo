import json


# 版图 territory
def territory_drc(file_path):
    def parse_lines(temp):
        return {
            "Processing_Rule": temp[0].strip().split(":")[-1].strip(),
            "Rule_Violations": int(temp[1].strip().split(":")[-1].strip())
        }

    result = {"model_name": "", "errors": []}
    with open(file_path, "r") as f:
        next(f)
        result["model_name"] = next(f).strip().split("\\")[-1]
        for i, line in enumerate(f):
            if line.startswith("Processing Rule"):
                temp = [line]
            elif line.startswith("Rule Violations"):
                temp.append(line)
                result["errors"].append(parse_lines(temp))

    return json.dumps(result)


if __name__ == '__main__':
    territory_drc(r"C:\Users\star\Desktop\DRC\DRC\Design Rule Check - ProgramControll1_PCB_Short1.drc")
