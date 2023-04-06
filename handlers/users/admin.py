import asyncio
from aiogram import types
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from states.states import GPTState
from loader import dp, db, bot
import pandas as pd

@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = await db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[-1])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)
       

@dp.message_handler(text="/reklama", user_id=ADMINS, state="*")
async def get_optional_ad(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Menga reklama uchun ixtiyoriy xabar jo'nating va men uni foydalanuvchilarga jo'nataman.")
    await GPTState.get_ads.set()

@dp.message_handler(state=GPTState.get_ads, content_types=['photo', 'video', 'document', 'sticker'])
async def send_optional_ad(message: types.Message, state: FSMContext):    
    users = await db.select_all_users()
    try:
        for user in users:
            user_id = user[3]
            try:
                await message.send_copy(chat_id=user_id)
                await asyncio.sleep(0.05)
            except Exception:
                await bot.send_message(chat_id=user_id,text=f"{user[1]} botni bloklagani uchun unga reklama bormadi")
                
    except Exception as error:
        print(error)
    finally:
        await message.answer(text="Reklama foydalanuvchilarga jo'natildi")
    await state.finish()

# @dp.message_handler(text="/reklama", user_id=ADMINS)
# async def send_ad_to_all(message: types.Message):
#     users = await db.select_all_users()
#     for user in users:
#         user_id = user[-1]
#         await bot.send_message(chat_id=user_id, text="@BekoDev kanaliga obuna bo'ling!")
#         await asyncio.sleep(0.05)

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    await db.delete_users()
    await message.answer("Baza tozalandi!")
