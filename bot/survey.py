#! bot/survey.py
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)

from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, filters
)

from bot.utils import two_keyboard_buttons

NAME, PHONE, STATUS, CHAR, CONSENT = range(5)

CONSENT_TEXT = (
    "Прежде чем завершить регистрацию,"
    "• пожалуйста подтвердите согласие:"
    "'Я согласен(на) на обработку моих персональных данных (ФИО, номер телефона) для участия в проекте и их передачу организаторам съёмок."
    "Данные будут храниться до окончания проекта."
    "Ответьте: «ДА» или «НЕТ».'"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте! Пожалуйста, укажите Фамилию Имя Отчество. ")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Укажите свой номер телефона")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("Напишите свой статус: групповка или АМС")
    return STATUS

async def get_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['status'] = update.message.text
    await update.message.reply_text("Укажите своего персонажа")
    return CHAR

async def get_char(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['char'] = update.message.text

    keyboard = two_keyboard_buttons(
        ["✅ Да, я согласен", "❌ Нет"], 
        ["consent_yes", "consent_no"]
    )
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
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_status)],
        CHAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_char)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
