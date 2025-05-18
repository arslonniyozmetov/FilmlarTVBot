from aiogram.dispatcher.filters.state import State, StatesGroup



class KinoQidiruv(StatesGroup):
    waiting_for_kino_id = State()
