from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder
from src.parser import get_institutes_abbrs


def generate_acronyms_reply_keyboard() -> ReplyKeyboardMarkup:
    acronyms = await get_institutes_abbrs()
    builder = KeyboardBuilder(button_type=KeyboardButton)
    for abbr in acronyms:
        builder.add(KeyboardButton(text=str(abbr)))
    builder.adjust(4)
    keyboard = ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True)
    return keyboard
