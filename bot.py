from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import ( 
    ApplicationBuilder, CommandHandler, MessageHandler, 
    filters, ContextTypes, ConversationHandler, CallbackQueryHandler
)
from models import Session, Participant
from config import TG_TOKEN

# NAME, AGE, HEIGHT, PHONE, PHOTO, CONSENT = range(6)
NAME, AGE, HEIGHT, PHONE, CONSENT = range(5)
CONSENT_TEXT = (
    "Прежде чем завершить регистрацию, пожалуйста подтвердите согласие:\n\n"
    "'☑️ Я согласен(на) на обработку моих персональных данных (ФИО, возраст, рост, и телефон) "
    "для участия в массовке и их передачу организаторам съёмок. "
    "Данные будут храниться до окончания проекта. Я могу отозвать согласие в любой момент.'\n\n"
    "Ответьте: «ДА» или «НЕТ»."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Как тебя зовут?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Сколько тебе лет?")
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['age'] = update.message.text
    await update.message.reply_text("Укажи свой рост (в см):")
    return HEIGHT

async def get_height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['height'] = update.message.text
    await update.message.reply_text("Твой номер телефона:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text

    keyboard = [
        [
            InlineKeyboardButton("✅ Да, я согласен", callback_data="consent_yes"),
            InlineKeyboardButton("❌ Нет", callback_data="consent_no"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
            CONSENT_TEXT,
            reply_markup=reply_markup,
    )

    return CONSENT

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

        # from sheets import add_participant_to_sheet
        # add_participant_to_sheet(
        #     context.user_data['name'],
        #     context.user_data['age'],
        #     context.user_data['height'],
        #     context.user_data['phone'],
        #     context.user_data['photo_id'],
        #     True,
        # )

        await query.edit_message_text("✅ Спасибо! Ты записан на массовку.")
    else:
        await query.edit_message_text("❌ Без согласия мы не можем продолжить. Регистрация отменена.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ок, отмена.")
    return ConversationHandler.END

app = ApplicationBuilder().token(TG_TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_height)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        # PHOTO: [MessageHandler(filters.PHOTO, get_photo)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(consent_callback, pattern="^consent_"))

if __name__ == "__main__":
    app.run_polling()
