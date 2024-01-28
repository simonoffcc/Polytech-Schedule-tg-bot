from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder
from src.parser.data_mining_methods import institutes_acronyms


def generate_acronyms_reply_keyboard() -> ReplyKeyboardMarkup:
    builder = KeyboardBuilder(button_type=KeyboardButton)
    for abbr in institutes_acronyms:
        builder.add(KeyboardButton(text=str(abbr)))
    builder.add(KeyboardButton(text="Отмена"))
    builder.adjust(4)
    keyboard = ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True)
    return keyboard
