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
    query = update.callback_query
    await query.answer()
    session = Session()
    selected_ids = context.user_data.get('selected_ids', set())
    sheet_title = context.user_data.get('sheet_title')
    if query.data == "confrm_yes":
        yes_participants = session.query(Participant).filter(
            Participant.confirmed.in_([ConfirmationStatus.no, ConfirmationStatus.yes]),
            Participant.telegram_id.in_(selected_ids)
        )
        for y_p in yes_participants:
            y_p.confirmed = ConfirmationStatus.yes

        sheet = get_sheet_by_title(sheet_title)        
        insert_in_certain_sheet(sheet)

    elif query.data == "confirm_no":
        await query.edit_message_text("❗ Обязательно предупредите бригадира.")

    return ConversationHandler.END



