# ingest.py
import json
import uuid
from embed_model import Embedder
from vectorstore import QdrantStore

# Replace with your dataset path
DATASET_PATH = "math_kb.json"

def load_dataset(path):
    with open(path, 'r', encoding='utf8') as f:
        data = json.load(f)
    # data expected: list of {"id":..., "question":..., "answer":..., "steps": "..."}
    return data

def build_kb(dataset_path=DATASET_PATH):
    embed = Embedder()
    store = QdrantStore()
    sample = load_dataset(dataset_path)
    # compute vectors in batches
    texts = [item['question'] + " ||| " + item.get("answer","") for item in sample]
    vectors = embed.encode(texts)
    # create the collection
    store.create_collection(vector_size=vectors.shape[1])
    ids = [item.get("id", str(uuid.uuid4())) for item in sample]
    payloads = [{"question": item["question"], "answer": item.get("answer",""), "steps": item.get("steps","")} for item in sample]
    store.upsert_items(ids, vectors, payloads)
    print("Ingested", len(sample), "items into Qdrant")

if __name__ == "__main__":
    build_kb()
