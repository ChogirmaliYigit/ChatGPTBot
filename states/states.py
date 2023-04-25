from aiogram.dispatcher.filters.state import StatesGroup, State


class GPTState(StatesGroup):
    start = State()
    new_chat = State()
    chat_list = State()
    continue_chat = State()
    edit_new_chat_title = State()
    edit_old_chat_title = State()
    get_ads = State()


class DalleState(StatesGroup):
    get_prompt = State()
    get_num = State()
    get_model = State()