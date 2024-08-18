import os
import json
import faiss
import logging
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer
import torch

# Load JSON
def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

# Normalize the vectors
def normalize_vector(v):
    return v / np.linalg.norm(v)

# Segment articles into paragraphs
def segment_article(article_text):
    # This is a simple segmentation; consider more sophisticated methods if needed
    return article_text.split("\n")

# Encoding with Sentence Transformer
def encode_with_sentence_transformer(model, text):
    segments = segment_article(text)
    segment_embeddings = model.encode(segments)
    # Mean-pooling for the segments
    aggregated_embedding = np.mean(segment_embeddings, axis=0)
    return normalize_vector(aggregated_embedding).astype('float32')

model = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')
if torch.cuda.is_available():
    model = model.to(torch.device("cuda"))

# Logging setup
today = datetime.now().strftime("%Y-%m-%d")
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, f"log_{today}.txt"), level=logging.INFO)

# Data and indexes setup
data_dir = today
index_dir = "indexes"
today_index_dir = os.path.join(index_dir, today)
os.makedirs(today_index_dir, exist_ok=True)

index_path = os.path.join(today_index_dir, "consolidated.index")
mapping_path = os.path.join(today_index_dir, "consolidated_mapping.json")

doc_vectors = []
mapping = {}
total_articles = 0

# Indexing loop
for subdir in os.listdir(data_dir):
    json_files = []
    
    for path, _, files in os.walk(os.path.join(data_dir, subdir)):
        for name in files:
            if name.endswith(".json"):
                json_files.append(os.path.join(path, name))

    for idx, json_file in enumerate(json_files):
        data = load_json(json_file)
        article_text = data.get('article')
        
        if article_text is None:
            continue
        
        encoded = encode_with_sentence_transformer(model, article_text)
        
        if encoded.size == 0:
            continue

        doc_vectors.append(encoded)
        mapping[total_articles] = json_file
        total_articles += 1

    logging.info(f"Finished index for {subdir}")

# Create consolidated index
doc_vectors = np.vstack(doc_vectors)
index = faiss.IndexFlatIP(doc_vectors.shape[1])
index = faiss.IndexIDMap(index)
index.add_with_ids(doc_vectors, np.array(range(len(doc_vectors))))
faiss.write_index(index, index_path)

with open(mapping_path, 'w') as f:
    json.dump(mapping, f)

print(f"Final lengths - doc_vectors: {len(doc_vectors)}, mapping: {len(mapping)}")
logging.info("Script complete")
