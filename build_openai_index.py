import os
import json
from load_all import load_all_docs
from tqdm import tqdm
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text[:8191]  # limit to max input length
    )
    return response.data[0].embedding

def build_index():
    docs = load_all_docs()
    index = []

    for doc in tqdm(docs, desc="Embedding documents"):
        try:
            embedding = embed_text(doc["text"])
            index.append({
                "embedding": embedding,
                "text": doc["text"],
                "url": doc["url"]
            })
        except Exception as e:
            print(f"❌ Failed to embed document: {e}")

    with open("openai_index.json", "w", encoding="utf-8") as f:
        json.dump(index, f)

    print(f"✅ Indexed {len(index)} documents with OpenAI embeddings.")

if __name__ == "__main__":
    build_index()
