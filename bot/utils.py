from datetime import datetime, timedelta
from functools import wraps
from telegram import (
    InlineKeyboardMarkup, InlineKeyboardButton, Update
)
from telegram.ext import ContextTypes

from config import TG_ADMINS

def make_sheet_title():
    d = datetime.now()
    d += timedelta(days=1)
    str_d = d.date().isoformat()
    sheet_title = f"Вызов {str_d}"
    return sheet_title

def two_keyboard_buttons(btn_titles:list[str], cbk_datas:list[str]):
    keyboard = [
        [
            InlineKeyboardButton(btn_titles[0], callback_data=cbk_datas[0]),
            InlineKeyboardButton(btn_titles[1], callback_data=cbk_datas[1])
        ]        
    ]
    return keyboard

def admin_only(handler_func):
    @wraps(handler_func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in TG_ADMINS:
            if update.message:
                await update.message.reply_text("🚫 Доступ закрыт.")
            elif update.callback_query:
                await update.callback_query.answer("🚫 Доступ закрыт.", show_alert=True)
            return
        return await handler_func(update, context, *args, **kwargs)
    return wrapper
