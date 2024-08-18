import os
import json
from datetime import datetime
import re
from unidecode import unidecode

def strip_non_ascii(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for key, value in data.items():
        if isinstance(value, str):
            # Translate string to ASCII
            value = unidecode(value)
            # Remove newline characters and replace with space
            value = value.replace("\n", " ")
            # Remove tab characters
            value = value.replace("\t", "")
            # Replace Unicode right single quotation mark with an ASCII apostrophe
            value = re.sub(r'\u2019', "'", value)
            # Replace encoded double quotes with ASCII double quotes
            value = value.replace('\\"', '"')
            data[key] = value

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

if __name__ == '__main__':
    today = datetime.now().strftime("%Y-%m-%d")
    root_folder = today

    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.json'):
                full_path = os.path.join(subdir, file)
                strip_non_ascii(full_path)
