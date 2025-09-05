import os, os.path as p, requests, chromadb
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# .env z ustawieniami Ollama
load_dotenv(p.expanduser("~/RAG_local/.env"))

OLLAMA = os.getenv("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.getenv("OLLAMA_EMBED", "embeddinggemma")
LLM_MODEL = os.getenv("OLLAMA_LLM", "gemma2:2b")

INDEX_PATH = p.expanduser("~/RAG_local/index")
client = chromadb.PersistentClient(path=INDEX_PATH)
col = client.get_or_create_collection("docs")

app = FastAPI(title="RAG Local API (Ollama)")

class AskIn(BaseModel):
    query: str
    k: int = 2
    max_ctx_chars: int = 1200

class IngestIn(BaseModel):
    doc_id: str
    text: str

def embed(texts):
    r = requests.post(f"{OLLAMA}/api/embed",
                      json={"model": EMBED_MODEL, "input": texts},
                      timeout=120)
    r.raise_for_status()
    return r.json()["embeddings"]

def chat(messages) -> str:
    r = requests.post(f"{OLLAMA}/api/chat",
                      json={"model": LLM_MODEL, "messages": messages, "stream": False},
                      timeout=180)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, dict):
        msg = data.get("message")
        if isinstance(msg, dict):
            return str(msg.get("content", "")).strip()
        msgs = data.get("messages")
        if isinstance(msgs, list) and msgs:
            return str(msgs[-1].get("content", "")).strip()
    return str(data).strip()

@app.post("/ingest")
def ingest(item: IngestIn):
    vec = embed([item.text])[0]
    col.add(documents=[item.text], embeddings=[vec], ids=[item.doc_id])
    return {"status": "ok", "count": col.count()}

@app.post("/ask", response_class=PlainTextResponse)
def ask(body: AskIn):
    qvec = embed([body.query])[0]
    res = col.query(query_embeddings=[qvec], n_results=max(1, min(body.k, 12)))
    docs = res["documents"][0] if res["documents"] else []

    # zbuduj JEDEN zwarty kontekst bez śmieci
    ctx_parts, acc = [], 0
    for d in docs:
        if acc >= body.max_ctx_chars:
            break
        take = d[: max(0, body.max_ctx_chars - acc)]
        if take:
            clean = " ".join(take.split())
            ctx_parts.append(clean)
            acc += len(take)
    context = " ".join(ctx_parts) if ctx_parts else "brak danych"

    messages = [
        {"role": "system", "content": "Piszesz po polsku. Korzystaj z KONTEKSTU do zrozumienia tematu, a potem uzupelniaj swoją wiedzą z danych treningowych." 
                                      "Jeśli czegoś nie jesteś pewien, ale masz pomysł to oznacz to jako HIPOTEZA."},
        {"role": "user",
         "content": f"Pytanie: {body.query}\n\nKONTEKST:\n{context}"}
    ]
    return chat(messages)
