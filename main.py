from fastapi import FastAPI
from pydantic import BaseModel
from Local_Implementation import get_subthreads_for_question, generate_final_answer
import faiss


app = FastAPI()

class Query(BaseModel):
    question: str
    image: str = None

@app.post("/")
def answer_question(query: Query):
    results = get_subthreads_for_question(query.question, top_k=3)
    answer = generate_final_answer(query.question, results)

    links = [
        {
            "url": r.get("topic_url", ""),
            "text": r.get("topic_title", "Relevant post")
        } for r in results
    ]

    return {
        "answer": answer,
        "links": links
    }


"""with open("tds_discourse.meta.json", "r") as f:
    metadata = json.load(f)"""

def search_faiss(query_embedding, top_k=3):
    faiss.normalize_L2(query_embedding)
    D, I = index.search(query_embedding.astype("float32"), top_k)
    return [metadata[i] for i in I[0]]

