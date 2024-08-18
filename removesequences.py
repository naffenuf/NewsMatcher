import os
import json
from datetime import datetime

def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json_str = json.dumps(data, ensure_ascii=False)
        json_str = json_str.replace('\\"', '"')  # Remove escaped quotes
        f.write(json_str)

def process_files_in_subfolders(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                
                # Read JSON file
                data = read_json_file(filepath)
                
                # Write the modified JSON back to the file
                write_json_file(filepath, data)

if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')  # Get today's date
    root_folder = f'./{today}'  # Change to your base directory
    
    # Verify that the folder exists
    if os.path.exists(root_folder) and os.path.isdir(root_folder):
        process_files_in_subfolders(root_folder)
    else:
        print(f"The folder {root_folder} does not exist.")
