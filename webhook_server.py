# webhook_server.py
from fastapi import FastAPI, Request
from telegram import Update
from bot import app as telegram_app  # тут должен быть твой telegram Application
import asyncio

app = FastAPI()

@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
