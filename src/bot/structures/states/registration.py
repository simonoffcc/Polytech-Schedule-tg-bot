from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    choosing_institute = State()
    choosing_group_number = State()
