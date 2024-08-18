import os
import json
from datetime import datetime
from searchindexes import search_documents 

def store_results_in_json(filename, search_term, matching_files):
    # Create subfolder 'tests' if it doesn't exist
    subfolder_path = 'matches'
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        
    # Set JSON file path to be inside the 'tests' subfolder
    json_file_path = os.path.join(subfolder_path, 'matches.json')
    
    # Load existing data or initialize an empty list
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []
        
    # Create a new entry
    new_entry = {
        "filename": filename,
        "search-term": search_term,
        "matching-files": matching_files
    }
    
    # Add the new entry to existing data
    existing_data.append(new_entry)
    
    # Write updated data back to the JSON file
    with open(json_file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

# Get today's date in the required format
today = datetime.now().strftime("%Y-%m-%d")
directory_path = os.path.join(".", today)

# Loop through all subfolders in the directory for today's date
for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file.endswith(".json"):
            json_file_path = os.path.join(root, file)
            
            # Load the JSON file
            json_data = load_json(json_file_path)
            
            # Extract the first 100 words from the "article" key
            article_text = json_data.get('article', '')
            search_term = " ".join(article_text.split()[:100])
            
            # Run the search_documents function
            matching_files = search_documents(search_term)
            
            # Store the results in the matches.json file inside the 'tests' subfolder
            store_results_in_json(file, search_term, matching_files)
