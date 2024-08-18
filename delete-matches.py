import os

def delete_json_file():
    # Path to the subfolder 'tests' and the JSON file
    subfolder_path = 'matches'
    json_file_path = os.path.join(subfolder_path, 'matches.json')
    
    # Check if the JSON file exists and delete it
    if os.path.exists(json_file_path):
        os.remove(json_file_path)
        print(f"Deleted the file: {json_file_path}")
    else:
        print(f"The file {json_file_path} does not exist.")

# Run the function to delete the JSON file
delete_json_file()
