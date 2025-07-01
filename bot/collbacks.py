from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import ( 
    ApplicationBuilder, CommandHandler, MessageHandler, 
    filters, ContextTypes, ConversationHandler, CallbackQueryHandler
)
from models import Session, Participant
from config import TG_TOKEN

async def consent_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "consent_yes":
        context.user_data['consent'] = True

        session = Session()
        participant = Participant(
            name=context.user_data['name'],
            age=int(context.user_data['age']),
            height=int(context.user_data['height']),
            phone=context.user_data['phone'],
            photo_id=1,
            consent=True,
        )
        session.add(participant)
        session.commit()

        from sheets import add_participant_to_sheet
        add_participant_to_sheet(
            context.user_data['name'],
            context.user_data['age'],
            context.user_data['phone'],
            True,
        )

        await query.edit_message_text("✅ Спасибо! Ты записан на массовку.")
    else:
        await query.edit_message_text("❌ Без согласия мы не можем продолжить. Регистрация отменена.")

    return ConversationHandler.END



