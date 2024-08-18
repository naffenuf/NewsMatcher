import os
import json
import faiss
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer

# Normalize the vectors
def normalize_vector(v):
    return v / np.linalg.norm(v)

# Load JSON
def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

# Save JSON
def save_json(data, filepath):
    with open(filepath, 'a') as f:
        json.dump(data, f)
        f.write('\n')  # Ensures each entry is on a new line

# Segment articles into paragraphs
def segment_article(article_text):
    return article_text.split("\n")

# Encoding with Sentence Transformers to match indexing process
def encode_with_sentence_transformer(model, text):
    segments = segment_article(text)
    segment_embeddings = model.encode(segments)
    aggregated_embedding = np.mean(segment_embeddings, axis=0)
    return normalize_vector(aggregated_embedding).astype('float32')

# Initialize Sentence Transformer
model = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')

# Configuration
index_dir = "indexes"
similarity_threshold = 0.7
log_dir = "logs"

def search_documents(search_term):
    matching_files = []
    
    encoded_query = encode_with_sentence_transformer(model, search_term)
    encoded_query = np.expand_dims(encoded_query, axis=0)

    date = datetime.now().strftime("%Y-%m-%d")
    date_index_dir = os.path.join(index_dir, date)
    index_path = os.path.join(date_index_dir, "consolidated.index")
    mapping_path = os.path.join(date_index_dir, "consolidated_mapping.json")
    log_path = os.path.join(log_dir, f"search_log_{date}.txt")

    if not os.path.exists(date_index_dir) or not os.path.exists(mapping_path):
        print("Directory or mapping file does not exist. Exiting.")
        return matching_files

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    index = faiss.read_index(index_path)
    mapping = load_json(mapping_path)
    D, I = index.search(encoded_query, k=10)

    search_log = {"query": search_term, "results": []}
    
    for i, (d, sim) in enumerate(zip(I[0], D[0])):
        if sim > similarity_threshold:
            original_json_file = mapping.get(str(d), None)
            if original_json_file:
                json_data = load_json(original_json_file)
                cleaned_filename = original_json_file.split('/')[-1]
                full_text = json_data.get('article', 'N/A')

                search_log['results'].append({
                    "file": cleaned_filename,
                    "similarity": float(sim),
                    "URL": json_data.get('url', 'N/A'),
                    "matching_span": full_text[:200]  # Adjusted snippet size
                })
                matching_files.append(cleaned_filename)

    # Ensure complete JSON log
    with open(log_path, 'a') as f:
        json.dump(search_log, f)
        f.write('\n')

    return matching_files

# Example usage
# search_term = "Your search term here"
# result_files = search_documents(search_term)
# print("Result files:", result_files)
