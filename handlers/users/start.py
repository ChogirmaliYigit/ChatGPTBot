from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.gpt import markup
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    name = message.from_user.username
    full_name = message.from_user.full_name
    user = await db.select_user(telegram_id=message.from_user.id)
    if user is None:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=full_name,
            username=message.from_user.username,
        )
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"@{user[2]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
    # user = await db.select_user(telegram_id=message.from_user.id)
    else:
        await bot.send_message(chat_id=ADMINS[0], text=f"@{name} bazaga oldin qo'shilgan")
    if full_name.startswith('<') and full_name.endswith('>'):
        await message.answer(f"Assalomu aleykum!\n\n<i>Xush kelibsiz sizni qiziqtirgan mavzu bo'yicha yordam berishim mumkin!</i>", parse_mode=types.ParseMode.HTML, reply_markup=markup)
    else:
        await message.answer(f"Assalomu aleykum <b>{full_name}</b>!\n\n<i>Xush kelibsiz sizni qiziqtirgan mavzu bo'yicha yordam berishim mumkin!</i>", parse_mode=types.ParseMode.HTML, reply_markup=markup)