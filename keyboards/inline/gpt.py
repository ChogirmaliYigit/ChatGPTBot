from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.img_models import models


def make_chats_markup(chats):
    markup = InlineKeyboardMarkup(row_width=2)
    for chat in chats:
        markup.insert(InlineKeyboardButton(text=chat[1], callback_data=chat[0]))
        markup.insert(InlineKeyboardButton(text=f'❌ {chat[1]}', callback_data=f'delete_{chat[0]}'))
    return markup

def make_image_num_markup(number=1):
    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(InlineKeyboardButton(text="➖", callback_data=f'remove_{number}'))
    markup.insert(InlineKeyboardButton(text=f'{number}', callback_data=f'number_{number}'))
    markup.insert(InlineKeyboardButton(text="➕", callback_data=f'add_{number}'))
    markup.insert(InlineKeyboardButton(text="✅ Tayyor", callback_data=f'ready_{number}'))
    return markup

def make_image_model_markup(number, model=0):
    markup = InlineKeyboardMarkup(row_width=3)
    markup.insert(InlineKeyboardButton(text="⬅️", callback_data=f'previous_{model}'))
    markup.insert(InlineKeyboardButton(text=f'{models[model]}', callback_data=f'model_{models[model]}'))
    markup.insert(InlineKeyboardButton(text="➡️", callback_data=f'next_{model}'))
    markup.insert(InlineKeyboardButton(text="✅ Tayyor", callback_data=f'ready_{number}_{model}'))
    return markup
