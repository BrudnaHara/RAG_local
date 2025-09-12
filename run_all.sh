#!/bin/bash
set -euo pipefail
cd ~/RAG_local
source ./venv/bin/activate
set -a
[ -f ./.env ] && . ./.env
set +a
uvicorn --app-dir . rag_local_api:app --host 127.0.0.1 --port 8000 &
API_PID=$!
python3 tg_bot.py
kill $API_PID || true
