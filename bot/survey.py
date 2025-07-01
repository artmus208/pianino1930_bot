from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)

from telegram.ext import (
    ContextTypes, ConversationHandler, ConversationHandler, CommandHandler,
    MessageHandler, filters
)

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

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ок, отмена.")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_height)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)