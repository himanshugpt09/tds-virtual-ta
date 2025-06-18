import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# === Load precomputed embeddings ===
with open("tds_chunks_with_embeddings.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Convert embeddings to NumPy array
embeddings = np.array([m["embedding"] for m in metadata], dtype="float32")

# Normalize and build FAISS index
faiss.normalize_L2(embeddings)
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

# Load embedding model (only for query embedding)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# === Retrieval function ===
def get_subthreads_for_question(query, top_k=3):
    query_emb = embed_model.encode(query, convert_to_numpy=True)
    query_emb = query_emb / np.linalg.norm(query_emb)
    D, I = index.search(np.array([query_emb], dtype="float32"), top_k)
    results = [metadata[i] for i in I[0]]
    return results

# === Load generator model (Flan-T5) ===
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

gen_model_name = "google/flan-t5-large"  # Smaller than flan-t5-xxl
tokenizer = AutoTokenizer.from_pretrained(gen_model_name)
model_gen = AutoModelForSeq2SeqLM.from_pretrained(gen_model_name)

# === Answer generation function ===
def generate_final_answer(query, results, max_length=256):
    retrieved_texts = [r["chunk_text"] for r in results]
    context = "\n\n".join(retrieved_texts)
    prompt = f"Answer the question based on the following forum excerpts:\n\n{context}\n\nQuestion: {query}\nAnswer:"
    
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    outputs = model_gen.generate(**inputs, max_length=max_length)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
