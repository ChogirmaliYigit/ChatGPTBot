from aiogram.dispatcher.filters.state import StatesGroup, State


class GPTState(StatesGroup):
    start = State()
    new_chat = State()
    chat_list = State()
    continue_chat = State()
    edit_new_chat_title = State()
    edit_old_chat_title = State()