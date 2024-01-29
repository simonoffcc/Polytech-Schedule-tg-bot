from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    institute_choice = State()
    group_choice = State()
    confirmation = State()
