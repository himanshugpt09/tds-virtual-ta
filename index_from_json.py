import json
import numpy as np
import faiss

def load_embeddings(json_path, id_key="chunk_id", embed_key="embedding"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    ids = [d[id_key] for d in data]
    texts = [d.get("content") or d.get("chunk_text") for d in data]
    embeddings = np.array([d[embed_key] for d in data], dtype="float32")
    return ids, texts, embeddings, data

def build_faiss_index(embeddings):
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index

# Example usage:
ids, texts, emb, meta = load_embeddings("tds_chunks_with_embeddings.json")
index = build_faiss_index(emb)

# Save index and metadata if needed
faiss.write_index(index, "tds_discourse.index")
with open("tds_discourse.meta.json", "w") as f:
    json.dump(meta, f)
