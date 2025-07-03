from telegram.ext import (
    ApplicationBuilder, CallbackQueryHandler, CommandHandler
)

from .notifications import notify_all

from config import TG_TOKEN

app = ApplicationBuilder().token(TG_TOKEN).build()

from .survey import conv_handler

from .collbacks import consent_callback, confirm_callback

app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(consent_callback, pattern="^consent_"))
app.add_handler(CommandHandler("notify", notify_all))


from .admin_panel import panel_conv, send_one_handler


app.add_handler(panel_conv)
app.add_handler(send_one_handler)

