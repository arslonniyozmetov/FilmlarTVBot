from aiogram.dispatcher.filters.state import State, StatesGroup

class AddMovie(StatesGroup):
    WaitingForMovie = State()
    WaitingForName = State()
    WaitingForGenre = State()
    WaitingForLanguage = State()
    WaitingForQuality = State()
    WaitingForCountry = State()
    WaitingForYear = State()
    WaitingForDuration = State()
    WaitingForRating = State()

class EditMovie(StatesGroup):
    WaitingForText = State()
    WaitingForVideo = State()

class AddChannel(StatesGroup):
    WaitingForChannelLink = State()
