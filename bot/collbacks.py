from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from models import Session, Participant, ConfirmationStatus
from sheets import insert_in_certain_sheet, get_sheet_by_title


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


async def confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("In...confirm_callback...")
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    session = Session()
    sheet_title = context.user_data.get('sheet_title')
    if query.data == "confirm_yes":
        yes_participant = session.query(Participant).filter(
            Participant.telegram_id == user_id
        ).one()
        yes_participant.confirmed = ConfirmationStatus.yes
        session.add(yes_participant)
        session.commit()
        sheet = get_sheet_by_title(sheet_title)        
        insert_in_certain_sheet(
            sheet,
            yes_participant.name,
            yes_participant.phone,
            yes_participant.status,
            yes_participant.char,
            yes_participant.consent,
            time_created=datetime.now().isoformat(sep=" ")
        )
        await query.edit_message_text("✅ Спасибо! Будем ждать вас на площадке.")
    elif query.data == "confirm_no":
        await query.edit_message_text("❗ Обязательно предупредите бригадира.")

    return ConversationHandler.END



