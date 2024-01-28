from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TO_MENU_BTN = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="На главное меню")],
],
    resize_keyboard=True)
