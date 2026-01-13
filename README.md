# RAG_local

Lokalny RAG (Retrieval-Augmented Generation) z wykorzystaniem Chroma (wektory) + Ollama (LLM/embeddings) + FastAPI (API endpoints) + bot Telegram.

## Wymagania

- Linux, Python 3.11+ (testowane na Debian 13)
- Ollama 0.11.10 (API na 127.0.0.1:11434)
- Model LLM: gemma2:2b (lub inny w .env)
- Embeddings: embeddinggemma (lub inny w .env)


# RAG_local

Lokalny RAG (Retrieval-Augmented Generation) z wykorzystaniem Chroma (wektory) + Ollama (LLM/embeddings) + FastAPI (API endpoints) + bot Telegram.

## Wymagania

- Linux, Python 3.11+ (testowane na Debian 13)
- Ollama 0.11.10 (API na 127.0.0.1:11434)
- Model LLM: gemma2:2b (lub inny w .env)
- Embeddings: embeddinggemma (lub inny w .env)

## Instalacja

git clone https://github.com/BrudnaHara/RAG_local.git
cd RAG_local
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Konfiguracja

Utwórz plik .env:

TG_BOT_TOKEN=TU_TOKEN_Z_BOTFATHER
RAG_K=3
RAG_CTX=1500
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_EMBED=embeddinggemma
OLLAMA_LLM=gemma2:2b


## API

### POST /ask

Body:
{"query":"...","k":3,"max_ctx_chars":1500}

Zwraca czysty tekst odpowiedzi.

### POST /ingest

Body:
{"doc_id":"id","text":"pełny_tekst"}

Dodaje dokument do Chroma.

## Notatki

- .env, index/, logs/, .pids/ są ignorowane przez Git
- Prompt systemowy wymusza język polski i oznaczanie niepewności jako HIPOTEZA
- Parametry RAG_K i RAG_CTX można nadpisywać w .env



- Prompt systemowy wymusza język polski i oznaczanie niepewności jako HIPOTEZA
- Parametry RAG_K i RAG_CTX można nadpisywać w .env
