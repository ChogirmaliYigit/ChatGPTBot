import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from utils.chat_gpt import chat_with_gpt
from states.states import GPTState
from keyboards.inline.gpt import make_chats_markup
from keyboards.default.gpt import markup, close_chat_markup



@dp.message_handler(text='❌ Chatni yakunlash', state='*')
async def close_chat(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="<b>Men sizni qiziqtirgan mavzu bo'yicha yordam berishim mumkin!</b>", reply_markup=markup)
    await GPTState.start.set()

@dp.message_handler(text='✏️ Chat nomini o\'zgartirish', state=GPTState.continue_chat)
async def edit_chat_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text=f"Chatning hozirgi nomi <code>{data.get('old_chat_title')}</code>\n\nYangilamoqchi bo'lgan nomingizni kiriting")
    await GPTState.edit_old_chat_title.set()

@dp.message_handler(text='✏️ Chat nomini o\'zgartirish', state=GPTState.new_chat)
async def edit_chat_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text=f"Chatning hozirgi nomi <code>{data.get('new_chat_title')}</code>\n\nYangilamoqchi bo'lgan nomingizni kiriting")
    await GPTState.edit_new_chat_title.set()

@dp.message_handler(state=GPTState.edit_new_chat_title)
async def get_new_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await db.update_chat_title(title=message.text, user_id=message.from_user.id, id=data.get('new_chat_id'))
    await message.answer(text=f"Chat nomi <code>{message.text}</code> ga yangilandi!\n\n<i>Suhbatlashishda davom eting</i>")
    await GPTState.new_chat.set()

@dp.message_handler(state=GPTState.edit_old_chat_title)
async def get_new_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await db.update_chat_title(title=message.text, user_id=message.from_user.id, id=data.get('old_chat_id'))
    await message.answer(text=f"Chat nomi <code>{message.text}</code> ga yangilandi!\n\n<i>Suhbatlashishda davom eting</i>")
    await GPTState.continue_chat.set()

@dp.message_handler(text="➕ Yangi Chat", state='*')
async def start_new_chat(message: types.Message, state: FSMContext):
    await state.finish()
    chats = await db.select_user_chats(user_id=message.from_user.id)
    await db.add_chat(user_id=message.from_user.id, title=f'Chat - {len(chats)+1}')
    await state.update_data({'new_chat_id': len(chats)+1, 'new_chat_title': f'Chat - {len(chats)+1}'})
    await message.answer(text="<b>Qiziqtirgan savolingiz bo'lsa menga yozing!</b>", reply_markup=close_chat_markup)
    await GPTState.new_chat.set()


@dp.message_handler(state=GPTState.new_chat)
async def get_user_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    # await state.update_data({'chat_id': int(data.get('new_chat_id'))})
    await db.add_message(message=message.text, chat_id=int(data.get('new_chat_id')), type='user')

    message_history = await db.select_chat_messages(chat_id=data.get('new_chat_id'))
    messages = []
    for msg in message_history:
        messages.append({'role': msg['type'], 'content': msg['message']})

    stickers = ['⏳', '⌛️']
    msg = await message.answer(text=stickers[-1])
    msg_id = msg.message_id

    for sticker in stickers:
        await asyncio.sleep(3.5)
        await bot.edit_message_text(text=sticker, chat_id=message.chat.id, message_id=msg_id)

    response = chat_with_gpt(messages=messages)
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    await message.answer(text=response)
    await db.add_message(message=response, chat_id=data.get('new_chat_id'), type='assistant')


@dp.message_handler(text='📝 Chatlar tarixi', state='*')
async def get_chat_list(message: types.Message, state: FSMContext):
    await state.finish()
    chats = await db.select_user_chats(user_id=message.from_user.id)
    if chats:
        await message.answer(text='<b>Sizning chatlaringiz quyidagilar:</b>', reply_markup=make_chats_markup(chats=chats))
        await GPTState.chat_list.set()
    else:
        await message.answer(text='<b>Sizda chatlar mavjud emas!</b>\n\n<i>Marhamat, yangi chat boshlang</i>', reply_markup=markup)
        await GPTState.start.set()


@dp.callback_query_handler(state=GPTState.chat_list)
async def get_chat(call: types.CallbackQuery, state: FSMContext):
    if call.data.split('_')[0] == 'delete':
        await db.delete_chat(id=int(call.data.split('_')[-1]))
        chats = await db.select_user_chats(user_id=call.from_user.id)
        if chats:
            await call.message.edit_text(text='<b>Sizning chatlaringiz quyidagilar:</b>', reply_markup=make_chats_markup(chats=chats))
        else:
            await call.message.delete()
            await call.message.answer(text='<b>Sizda chatlar mavjud emas!</b>\n\n<i>Marhamat, yangi chat boshlang</i>', reply_markup=markup)
            await GPTState.start.set()
    else:
        await call.message.delete()
        chat = await db.select_chat(id=int(call.data))
        await state.update_data({'old_chat_id': int(call.data), 'old_chat_title': chat[-1]})
        await call.message.answer(text="<b>Qiziqtirgan savolingiz bo'lsa menga yozing!</b>", reply_markup=close_chat_markup)
        await GPTState.continue_chat.set()


@dp.message_handler(state=GPTState.continue_chat)
async def get_user_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    # await state.update_data({'chat_id': data.get('old_chat_id')})
    await db.add_message(message=message.text, chat_id=int(data.get('old_chat_id')), type='user')
    
    message_history = await db.select_chat_messages(chat_id=data.get('new_chat_id'))
    messages = []
    for msg in message_history:
        messages.append({'role': msg['type'], 'content': msg['message']})

    stickers = ['⏳', '⌛️']
    msg = await message.answer(text=stickers[-1])
    msg_id = msg.message_id

    for sticker in stickers:
        await asyncio.sleep(3.5)
        await bot.edit_message_text(text=sticker, chat_id=message.chat.id, message_id=msg_id)

    response = chat_with_gpt(messages=messages)
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    await message.answer(text=response)
    await db.add_message(message=response, chat_id=data.get('old_chat_id'), type='assistant')
