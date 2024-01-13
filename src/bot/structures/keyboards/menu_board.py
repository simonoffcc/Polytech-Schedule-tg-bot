from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


MENU_BOARD = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Сегодня и завтра"), KeyboardButton(text="Текущая неделя")],
    [KeyboardButton(text="Помощь"), KeyboardButton(text="Следующая неделя")],
],
    resize_keyboard=True)
