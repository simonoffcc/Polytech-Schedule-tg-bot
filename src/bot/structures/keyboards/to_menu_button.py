from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TO_MENU_BTN = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="На главное меню")],
],
    resize_keyboard=True)

CANCEL_BUTTON = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отмена")],
],
    resize_keyboard=True)
