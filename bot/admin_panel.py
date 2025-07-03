

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters,
    CallbackQueryHandler
)

from .utils import admin_only
from models import Session, Participant
from sheets import create_new_sheet

PAGE_SIZE = 10

@admin_only
async def open_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Admin-Pannel is opened")
    session = Session()
    participants = session.query(Participant).all()
    total_pages = len(participants) // PAGE_SIZE
    # Сохраняем всех и обнуляем выбор
    context.user_data['all_users'] = {str(p.telegram_id): p.name for p in participants}
    context.user_data['selected_ids'] = set()
    context.user_data['current_page'] = 0

    # Отобразим первых 10 участников
    keyboard = []
    for p in participants[:10]:
        keyboard.append([
            InlineKeyboardButton(
                f"{p.name} {'✅' if str(p.telegram_id) in context.user_data['selected_ids'] else ''}",
                callback_data=f"select_{p.telegram_id}"
            )
        ])
    keyboard.append([InlineKeyboardButton("➡ Дальше", callback_data="next_page")])
    keyboard.append([InlineKeyboardButton("📨 Готово", callback_data="finish_selection")])

    await update.message.reply_text(
        f"Выберите участников для рассылки: 0/{total_pages}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    print("Admin-Pannel msg is rendered")
    return "SELECTING"



async def render_user_page(update_or_query, context):
    page = context.user_data['current_page']
    all_users = list(context.user_data['all_users'].items())
    count_pages = len(all_users) // PAGE_SIZE
    selected = context.user_data['selected_ids']
    print(f"Re-render Admin-Pannel page: {page} of {count_pages}")
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    visible_users = all_users[start:end]

    keyboard = []
    for uid, user in visible_users:
        keyboard.append([
            InlineKeyboardButton(
                f"{user} {'✅' if uid in selected else ''}",
                callback_data=f"select_{uid}"
            )
        ])

    nav_buttons = []
    if start > 0:
        nav_buttons.append(InlineKeyboardButton("⬅ Назад", callback_data="prev_page"))
    if end < len(all_users):
        nav_buttons.append(InlineKeyboardButton("➡ Вперёд", callback_data="next_page"))
    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append([InlineKeyboardButton("📨 Готово", callback_data="finish_selection")])

    if hasattr(update_or_query, 'edit_message_reply_markup'):
        await update_or_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update_or_query.message.reply_text(
            f"Выберите участников для рассылки: {page}/{count_pages}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    return "SELECTING"



# PASSED 
async def selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Selection-Callback start")
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("select_"):
        uid = data.split("_")[1]
        
        selected = context.user_data['selected_ids']

        if uid in selected:
            print(f"UnSelected: {uid}")
            selected.remove(uid)
        else:
            print(f"Selected: {uid}")
            selected.add(uid)

        return await render_user_page(query, context)
    
    elif data == "next_page":
        print("Next page in section callback...")
        context.user_data['current_page'] += 1
        return await render_user_page(query, context)
    

    elif data == "prev_page":
        print("Prev page in section callback...")
        context.user_data['current_page'] -= 1
        return await render_user_page(query, context)
    

    elif data == "finish_selection":
        print("selection_callback (finish_selection)")
        await query.edit_message_text("✍ Введите сообщение для выбранных участников:")
        return "WAITING_MESSAGE"

async def send_confirm_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    selected_ids = context.user_data.get('selected_ids', set())

    session = Session()
    participants = session.query(Participant).filter(Participant.telegram_id.in_(map(int, selected_ids))).all()

    count = 0
    keyboard = []
    for p in participants:
        keyboard.append([
            
        ])
        try:
            await context.bot.send_message(chat_id=p.telegram_id, text=message_text)
            count += 1
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    await update.message.reply_text(f"✅ Сообщение отправлено {count} участникам.")
    
    try:
        create_new_sheet()
        await update.message.reply_text(f"✅ В таблице создан новый лист под очередной вызов")
    except:
        await update.message.reply_text(f"❌ Ошибка создания листа ")

    return ConversationHandler.END


async def send_to_one(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Формат: /sendto <telegram_id> <сообщение>")
        return

    try:
        user_id = int(context.args[0])
        text = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=text)
        await update.message.reply_text("✅ Сообщение отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке: {e}")
        await update.message.reply_text("❌ Не удалось отправить сообщение.")

send_one_handler = CommandHandler("sendto", send_to_one)

panel_conv = ConversationHandler(
    entry_points=[CommandHandler("panel", open_panel)],
    states={
        "SELECTING": [
            CallbackQueryHandler(selection_callback, pattern="^(select_|finish_selection|next_page|prev_page)")
        ],
        "WAITING_MESSAGE": [
            MessageHandler(filters.TEXT & ~filters.COMMAND, send_confirm_message)
        ],
    },
    fallbacks=[]
)

