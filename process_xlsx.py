import pandas as pd
from pathlib import Path


def process_xlsx(file_path):
    data = pd.read_excel(r"C:\Users\star\Desktop\ProgramContro_1\ProgramControll1_SCH_BOM1.xlsx", engine="openpyxl")
    result = data.to_dict("records")

    return {
        "model_path": Path(file_path).stem,
        "BOM": result
    }


if __name__ == '__main__':
    result = process_xlsx(r"C:\Users\star\Desktop\ProgramContro_1\ProgramControll1_SCH_BOM1.xlsx")
    print(result)
