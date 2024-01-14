from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


MENU_BOARD = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сегодня и завтра'), KeyboardButton(text='Следующая неделя')],
    [KeyboardButton(text='Текущая неделя'), KeyboardButton(text='ℹ️ Info')],
],
    resize_keyboard=True)
