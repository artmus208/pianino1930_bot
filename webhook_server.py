# webhook_server.py
from fastapi import FastAPI, Request
from telegram import Update
from bot import app as telegram_app 
import asyncio

app = FastAPI()
is_initialized = False  # флаг для инициализации один раз

@app.on_event("startup")
async def startup():
    global is_initialized
    if not is_initialized:
        await telegram_app.initialize()
        is_initialized = True


@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
