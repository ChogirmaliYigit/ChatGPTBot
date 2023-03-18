from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup.insert(KeyboardButton(text="➕ Yangi Chat"))
markup.insert(KeyboardButton(text="📝 Chatlar tarixi"))

close_chat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
close_chat_markup.insert(KeyboardButton(text='❌ Chatni yakunlash'))
close_chat_markup.insert(KeyboardButton(text='✏️ Chat nomini o\'zgartirish'))
