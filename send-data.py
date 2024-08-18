import shutil
import os
import json
from datetime import datetime

def consolidate_json_files(folder_path):
    consolidated_data = {}
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                consolidated_data[file_name] = data
    return consolidated_data

# Get today's date in YYYY-MM-DD format
today_date = datetime.now().strftime('%Y-%m-%d')

# Path to the source files
source_folder_for_matches = os.path.join(os.getcwd(), 'matches')
source_file_for_matches = os.path.join(source_folder_for_matches, 'deduplicated_matches.json')
source_folder_for_articles = os.path.join(os.getcwd(), today_date)

# Path to the destination folder and subfolders
destination_folder = '/Users/craigboyce/Developer/NewsMediator/TodaysData'
destination_folder_for_matches = os.path.join(destination_folder, 'matches')
destination_folder_for_articles = os.path.join(destination_folder, 'articles')

# Create the destination folders if they don't exist
for folder in [destination_folder, destination_folder_for_matches, destination_folder_for_articles]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Copy deduplicated_matches.json
if os.path.exists(source_file_for_matches):
    shutil.copy2(source_file_for_matches, destination_folder_for_matches)

# Consolidate and move articles JSON files
if os.path.exists(source_folder_for_articles):
    consolidated_data = consolidate_json_files(source_folder_for_articles)
    destination_file_for_articles = os.path.join(destination_folder_for_articles, 'consolidated_articles.json')
    with open(destination_file_for_articles, 'w') as f:
        json.dump(consolidated_data, f, indent=4)
