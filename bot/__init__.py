from telegram.ext import ApplicationBuilder, CallbackQueryHandler
from config import TG_TOKEN

app = ApplicationBuilder().token(TG_TOKEN).build()

from survey import conv_handler

from .collbacks import consent_callback

app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(consent_callback, pattern="^consent_"))
