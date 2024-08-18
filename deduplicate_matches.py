import json
import os

def similarity(set1, set2):
    """Calculate the similarity score between two sets."""
    if not set1 or not set2:
        return 0
    intersection = set1.intersection(set2)
    return len(intersection) / min(len(set1), len(set2))

def deduplicate_matches(matches, threshold=0.1):
    """Deduplicate matches based on a similarity threshold."""
    i = 0
    while i < len(matches):
        j = i + 1
        while j < len(matches):
            set1 = set(matches[i]['matching-files'])
            set2 = set(matches[j]['matching-files'])
            if similarity(set1, set2) >= threshold:
                matches[i]['matching-files'] = list(set1.union(set2))
                matches.pop(j)
            else:
                j += 1
        i += 1
    return matches

print(f"Current working directory: {os.getcwd()}")

input_path = os.path.join('matches', 'matches.json')
output_path = os.path.join('matches', 'deduplicated_matches.json')

print(f"Reading from: {os.path.abspath(input_path)}")
print(f"Writing to: {os.path.abspath(output_path)}")

try:
    with open(input_path, 'r') as f:
        json_data = json.load(f)
    print(f"Successfully read {len(json_data)} records from {input_path}.")
except Exception as e:
    print(f"Failed to read from {input_path}. Error: {e}")

deduplicated_data = None
try:
    deduplicated_data = deduplicate_matches(json_data)
    print(f"Successfully deduplicated the data. {len(deduplicated_data)} unique groups remaining.")
except Exception as e:
    print(f"Failed to deduplicate data. Error: {e}")

if deduplicated_data:
    total_filenames_count = sum(len(group['matching-files']) for group in deduplicated_data)
    print(f"Total number of filenames (including duplicates) displayed in all groups: {total_filenames_count}")

    try:
        with open(output_path, 'w') as f:
            json.dump(deduplicated_data, f, indent=4)
        print(f"Deduplicated data has been saved to {output_path}.")
    except Exception as e:
        print(f"Failed to write to {output_path}. Error: {e}")
