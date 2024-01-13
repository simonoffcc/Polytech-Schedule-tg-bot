from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import KeyboardBuilder


async def generate_acronyms_reply_keyboard(acronyms: list) -> ReplyKeyboardMarkup:
    builder = KeyboardBuilder(button_type=KeyboardButton)
    for abbr in acronyms:
        builder.add(KeyboardButton(text=str(abbr)))
    builder.adjust(4)
    keyboard = ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True)
    return keyboard


main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Сегодня и завтра"), KeyboardButton(text="Текущая неделя")],
    [KeyboardButton(text="Помощь"), KeyboardButton(text="Следующая неделя")],
],
    resize_keyboard=True)

help_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="На главное меню")],
],
    resize_keyboard=True)


project_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Связь с разработчиком', url='t.me/simonoffcc')],
    [InlineKeyboardButton(text='Код проекта', url='github.com/simonoffcc/Polytech-Schedule-tg-bot')]
])
