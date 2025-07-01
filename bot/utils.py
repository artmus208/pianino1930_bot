from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def two_keyboard_buttons(btn_titles:list[str], cbk_datas:list[str]):
    keyboard = [
        [
            InlineKeyboardButton(btn_titles[0], callback_data=cbk_datas[0]),
            InlineKeyboardButton(btn_titles[1], callback_data=cbk_datas[1])
        ]        
    ]
    return keyboard