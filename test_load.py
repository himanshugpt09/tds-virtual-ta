from load_all import load_all_docs

if __name__ == "__main__":
    docs = load_all_docs()
    print(f"✅ Loaded {len(docs)} documents.")
    print("Sample document:")
    print(docs[0])
