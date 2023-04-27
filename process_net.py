import json


def process_net(file_path):
    result = {
        "PARTS_LIST": {},
        "NET_LIST": {}
    }
    with open(file_path, "r") as f:
        contents = f.readlines()

        parts_list_end = 0
        for i, line in enumerate(contents):
            if line.startswith("Comment") or line.startswith("PARTS LIST"):
                continue

            if line.startswith("EOS"):
                parts_list_end = i
                break

            splits = line.split()
            result["PARTS_LIST"][splits[2]] = {
                "FootPrintName": splits[1],
                "Comment": splits[0]
            }

        for line in contents[parts_list_end + 1:]:
            if line.startswith("NET LIST") or line == "\n" or line.startswith("EOS"):
                continue
            elif line.startswith("NODENAME"):
                temp = line
            else:
                inner = line.split()
                result["NET_LIST"][temp.split()[1]] = [inner[i] + "." + inner[i + 1] for i in
                                                       range(0, len(inner) - 1, 2)]
        return json.dumps(result)


if __name__ == '__main__':
    print(process_net(r"C:\Users\star\Desktop\ProgramContro_1\ProgramControll1_SCH_1.NET"))
