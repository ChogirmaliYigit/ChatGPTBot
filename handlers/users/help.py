from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = 'Bot ChatGPT 3.5 modeli asosida sizning savollaringizga javob beradi, muammolaringizni hal qiladi, foydali maslahatlar beradi. Botdan foydalanish bepul. /start'    
    await message.answer(text=text)
