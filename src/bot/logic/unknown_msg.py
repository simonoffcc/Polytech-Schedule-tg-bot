from aiogram import Router, types

from src.bot.structures.keyboards import MENU_BOARD

unknown_message = Router(name='unknown_message')


@unknown_message.message()
async def unknown_message_handler(message: types.Message) -> types.Message:
    return await message.answer('не понимаю тебя ._.', reply_markup=MENU_BOARD)
