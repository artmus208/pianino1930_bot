from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from models import Session, Participant, ConfirmationStatus


async def consent_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    query = update.callback_query
    await query.answer()

    if query.data == "consent_yes":
        context.user_data['consent'] = True

        session = Session()
        participant = Participant(
            name=context.user_data['name'],
            phone=context.user_data['phone'],
            status=context.user_data['status'],
            char=context.user_data['char'],
            consent=True,
            telegram_id=telegram_id,
            time_created=datetime.now()
        )
        session.add(participant)
        session.commit()

        from sheets import add_participant_to_sheet
        add_participant_to_sheet(
            name=context.user_data['name'],
            phone=context.user_data['phone'],
            status=context.user_data['status'],
            char=context.user_data['char'],
            time_created=datetime.now().isoformat(),
            consent=True,
        )

        await query.edit_message_text("✅ Спасибо! Будем ждать вас на площадке.")
    else:
        await query.edit_message_text("❌ Без согласия мы не можем продолжить. Регистрация отменена.")

    return ConversationHandler.END



