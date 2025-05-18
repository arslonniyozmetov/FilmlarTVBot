from aiogram.dispatcher.filters.state import State, StatesGroup


class Post(StatesGroup):
    text = State()
    kino = State()
    ID = State()
    video = State()