from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder


def generate_acronyms_reply_keyboard(acronyms: list) -> ReplyKeyboardMarkup:
    builder = KeyboardBuilder(button_type=KeyboardButton)
    for abbr in acronyms:
        builder.add(KeyboardButton(text=str(abbr)))
    builder.adjust(4)
    keyboard = ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True)
    return keyboard
