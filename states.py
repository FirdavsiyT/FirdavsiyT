from aiogram.dispatcher.filters.state import State, StatesGroup

class HolidaysForTheYearState(StatesGroup):
    country = State()
    year = State()
    year_error = State()

class DateState(StatesGroup):
    date = State()