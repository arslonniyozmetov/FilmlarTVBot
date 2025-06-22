from aiogram.dispatcher.filters.state import State, StatesGroup

class AddMovie(StatesGroup):
    WaitingForMovie = State()
    WaitingForName = State()
    WaitingForGenre = State()       # 🎞 Janr
    WaitingForLanguage = State()    # 🗣 Til
    WaitingForQuality = State()     # 📀 Sifat
    WaitingForCountry = State()     # 🌏 Davlat
    WaitingForYear = State()        # 📆 Yil
    WaitingForDuration = State()    # 🎥 Davomiyligi
    WaitingForRating = State()      # ⭐ Reyting

class AddChannel(StatesGroup):
    WaitingForChannelLink = State()
