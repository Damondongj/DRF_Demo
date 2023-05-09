import os
from pathlib import Path

TEMP_PATH = str(Path.cwd().parent) + "\\media\\temp_file"
print(TEMP_PATH)
if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)
