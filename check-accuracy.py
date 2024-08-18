import json
import os  # Importing the os module

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def calculate_percentage_of_matches(json_data):
    total_entries = 0
    successful_matches = 0
    
    for entry in json_data:
        total_entries += 1
        filename = entry.get("filename", "")
        matching_files = entry.get("matching-files", [])
        
        # Strip the folder name (date) from the beginning of each file in matching-files
        stripped_matching_files = [os.path.basename(f) for f in matching_files]
        
        if filename in stripped_matching_files:
            successful_matches += 1
    
    if total_entries == 0:
        return 0.0  # To avoid division by zero
    
    return (successful_matches / total_entries) * 100

if __name__ == "__main__":
    # Load matches.json
    json_file_path = os.path.join('matches', 'matches.json')
    
    if not os.path.exists(json_file_path):
        print("matches.json does not exist.")
    else:
        json_data = load_json(json_file_path)
        
        # Calculate the percentage of successful matches
        percentage = calculate_percentage_of_matches(json_data)
        
        print(f"The percentage of entries where 'matching-files' contains 'filename' is {percentage}%.")
