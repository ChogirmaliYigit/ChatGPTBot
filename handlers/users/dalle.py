from data.config import OPENAI_KEY
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from utils.chat_gpt import chat_with_gpt
from states.states import DalleState
from keyboards.inline.gpt import make_image_num_markup, make_image_model_markup
from keyboards.default.gpt import markup, close_chat_markup
from utils.dalle import generate_image
from utils.img_models import models


@dp.message_handler(text='/image', state='*')
async def get_data(message: types.Message, state: FSMContext):
    await message.answer(text="Rasm yaratish uchun kerakli ta'rifni yozing:")
    await DalleState.get_prompt.set()

@dp.message_handler(state=DalleState.get_prompt)
async def get_image_num(message: types.Message, state: FSMContext):
    await state.update_data({'prompt': message.text})
    await message.answer(text="Nechta rasm yaratmoqchisiz?\n\n<i><b>Rasmlar soni 1 dan 10 gacha bo'lishi shart!</b></i>", reply_markup=make_image_num_markup())
    await DalleState.get_num.set()

@dp.callback_query_handler(state=DalleState.get_num)
async def get_image_model(call: types.CallbackQuery, state: FSMContext):
    if call.data.startswith('ready'):
        number = int(call.data.split('_')[-1])
        await state.update_data({'number': number})
        await call.message.edit_text(text="Oxirgi qadam! Qaysi model asosida rasm yaratamiz.\n\n<i>Agar bu nima ekanini bilmasangiz, shunchaki ✅ Tayyor tugmasini bosing!</i>", reply_markup=make_image_model_markup(number=number))
        await DalleState.get_model.set()
    else:
        action, number = call.data.split('_')
        number = int(number)
        if action == 'add' and number < 10:
            await call.message.edit_reply_markup(reply_markup=make_image_num_markup(number=number+1))
        if action == 'remove' and number != 1:
            await call.message.edit_reply_markup(reply_markup=make_image_num_markup(number=number-1))
        else:
            pass

@dp.callback_query_handler(state=DalleState.get_model)
async def generating(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    prompt = data.get('prompt')
    number = int(data.get('number'))
    if call.data.startswith('ready'):
        model = call.data.split('_')[-1]
        await call.message.delete()
        await types.ChatActions.upload_photo()
        result = generate_image(openai_key=OPENAI_KEY, model=models[int(model)], prompt=prompt, num=number)
        if result == 'Xatolik':
            await call.message.answer(text="Rasm yaratishda xatolik yuz berdi. Birozdan keyin urinib ko'ring. Bu ta'rif yaxshi tushuntirilmaganidan yoki botda texnik ishlar olib borilayotganidan bo'lishi mumkin.")
            await DalleState.get_prompt.set()
        else:
            await call.answer(text='Yuklanmoqda...')
            await types.ChatActions.upload_photo()
            media = types.MediaGroup()
            for img in result['data']:
                media.attach_photo(photo=img['url'])
            await call.message.answer_media_group(media=media)
            await DalleState.get_prompt.set()
    else:
        action, model = call.data.split('_')
        model = int(model)
        if action == 'next' and model < 3:
            await call.message.edit_reply_markup(reply_markup=make_image_model_markup(number=number, model=model+1))
        if action == 'previous' and model != 0:
            await call.message.edit_reply_markup(reply_markup=make_image_model_markup(number=number, model=model-1))
        else:
            pass
    