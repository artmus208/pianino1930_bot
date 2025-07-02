from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import CommandHandler, ContextTypes
from .utils import admin_only

from models import Session, Participant
from config import TG_ADMINS

@admin_only
async def notify_all(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Напишите текст сообщения, например: /notify Съёмки завтра в 9:00" 
        )

    message_text = " ".join(context.args)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Подтверждаю", callback_data="confirm_yes"),
            InlineKeyboardButton("❌ Не подтверждаю", callback_data="confirm_no"),
        ]
    ])

    session = Session()
    participants = session.query(Participant).filter(
        Participant.telegram_id.isnot(None).all()
    )

    count = 0
    for p in participants:
        try:
            await context.bot.send_message(
                chat_id=p.telegram_id,
                text=message_text,
                reply_markup=keyboard
            )
            count += 1

        except Exception as e:
            print(f"Ошибка: {e}")
            

    await update.message.reply_text(f"✅ Сообщение отправлено {count} участникам.")


@admin_only
async def notify_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or '||' not in " ".join(context.args):
        await update.message.reply_text(
            "⚠️ Используй формат:\n/sendmsg id1 id2 id3 || сообщение"
        )
        return

    # Разделяем ID и сообщение
    raw = " ".join(context.args)
    id_part, text_part = raw.split("||", 1)
    ids = [int(x.strip()) for x in id_part.strip().split()]
    message = text_part.strip()

    count = 0
    for uid in ids:
        try:
            await context.bot.send_message(chat_id=uid, text=message)
            count += 1
        except Exception as e:
            print(f"Ошибка при отправке {uid}: {e}")

    await update.message.reply_text(f"✅ Сообщение отправлено {count} пользователям.")


