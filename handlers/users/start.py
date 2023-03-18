from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.gpt import markup
from states.states import GPTState


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    if name.startswith('<') and name.endswith('>'):
        user = await db.select_user(telegram_id=message.from_user.id)
        if user is None:
            user = await db.add_user(
                telegram_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username,
            )
            # ADMINGA xabar beramiz
            count = await db.count_users()
            msg = f"{name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
            await bot.send_message(chat_id=ADMINS[0], text=msg)
        # user = await db.select_user(telegram_id=message.from_user.id)
        else:
            await bot.send_message(chat_id=ADMINS[0], text=f"{name} bazaga oldin qo'shilgan")
        await message.answer(f"Assalomu aleykum <b>{name}</b>!\n\n<i>Xush kelibsiz sizni qiziqtirgan mavzu bo'yicha yordam berishim mumkin!</i>", reply_markup=markup)
        await GPTState.start.set()
    else:
        await message.answer(f"Assalomu aleykum!\n\n<i>Xush kelibsiz sizni qiziqtirgan mavzu bo'yicha yordam berishim mumkin!</i>", reply_markup=markup)
        await GPTState.start.set()