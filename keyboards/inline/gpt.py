from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def make_chats_markup(chats):
    markup = InlineKeyboardMarkup(row_width=2)
    for chat in chats:
        markup.insert(InlineKeyboardButton(text=chat[-1], callback_data=chat[0]))
        markup.insert(InlineKeyboardButton(text=f'❌ {chat[-1]}', callback_data=f'delete_{chat[0]}'))
    return markup