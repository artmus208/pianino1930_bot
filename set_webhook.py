# в отдельном скрипте или в main.py временно

from telegram import Bot
from config import TG_TOKEN
WEBHOOK_URL = "https://pianino1930.ru/webhook"

async def set_webhook():
    bot = Bot(TG_TOKEN)
    success = await bot.set_webhook(WEBHOOK_URL)
    print("Webhook set:", success)

import asyncio
asyncio.run(set_webhook())
