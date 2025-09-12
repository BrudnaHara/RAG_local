# RAG_local (Ollama + FastAPI + Telegram)

Lokalny RAG: Chroma (wektory) + Ollama (LLM/embeddings) + FastAPI (/ask, /ingest) + bot Telegram.

## Wymagania
- Linux, Python 3.11+ (testowane na Debian 13)
- Ollama `0.11.10` (API na `127.0.0.1:11434`)
- Model LLM: `gemma2:2b` (lub inny w `.env`)
- Embeddings: `embeddinggemma` (lub inny w `.env`)

## Instalacja
```bash
git clone https://github.com/BrudnaHara/RAG_local.git
cd RAG_local
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

###Konfiguracja
Utwórz ~/RAG_local/.env:
TG_BOT_TOKEN=TU_TOKEN_Z_BOTFATHER
RAG_K=3
RAG_CTX=1500
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_EMBED=embeddinggemma
OLLAMA_LLM=gemma2:2b

###Start (jednym poleceniem)
bash run_all.sh
To uruchamia:
FastAPI na http://127.0.0.1:8000
bota Telegram (long-polling)

###API
POST /ask
Body: {"query":"...", "k":3, "max_ctx_chars":1500}
Zwraca czysty tekst odpowiedzi.
POST /ingest
Body: {"doc_id":"id","text":"pełny_tekst"}
Dodaje dokument do Chroma.

###Notatki

.env, index/, logs/, .pids/ są ignorowane przez Git.
g
Prompt systemowy wymusza język polski i oznaczanie niepewności jako HIPOTEZA.

Parametry RAG_K i RAG_CTX można nadpisywać w .env.