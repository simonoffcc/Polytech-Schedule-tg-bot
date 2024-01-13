from aiogram import Router, types, F
from aiogram.filters import Command

from src.bot.structures.texts import help_text
from src.bot.structures.keyboards import DEVINFO_BOARD

help_router = Router(name='help')


@help_router.message(Command(commands=['help']))
@help_router.message(F.text == "Помощь")
async def help_handler(message: types.Message):
    return await message.answer(help_text, reply_markup=DEVINFO_BOARD)
