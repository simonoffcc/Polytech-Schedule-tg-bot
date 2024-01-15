from aiogram import Router, types

from src.bot.structures.message_texts import help_text
from src.bot.structures.keyboards import MENU_BOARD

unknown_message = Router(name='unknown_message')


@unknown_message.message()
async def unknown_message_handler(message: types.Message):
    return await message.answer(help_text, parse_mode='HTML', reply_markup=MENU_BOARD)
