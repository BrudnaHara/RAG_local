#!/usr/bin/env python3
# na górze pliku
import os, json, asyncio, httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv(os.path.expanduser("~/RAG_local/.env"))

API_URL = "http://127.0.0.1:8000/ask"
TOKEN = os.environ.get("TG_BOT_TOKEN")
K_DEFAULT = int(os.environ.get("RAG_K", "3"))
CTX_DEFAULT = int(os.environ.get("RAG_CTX", "1500"))


async def ask_rag(query: str, k: int = K_DEFAULT, max_ctx: int = CTX_DEFAULT) -> str:
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(API_URL, headers={"Content-Type":"application/json"},
                              content=json.dumps({"query": query, "k": k, "max_ctx_chars": max_ctx}))
        r.raise_for_status()
        return r.text.strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gotowa. Wyślij pytanie. Parametry: k=3, ctx=1500 (zmienisz RAG_K i RAG_CTX w env).")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text.strip()
    try:
        ans = await ask_rag(q)
    except Exception as e:
        ans = f"błąd: {e}"
    await update.message.reply_text(ans)

def main():
    if not TOKEN:
        raise SystemExit("Brak TG_BOT_TOKEN w env.")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
