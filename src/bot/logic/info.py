from aiogram import Router, types, F
from aiogram.filters import Command

from src.bot.structures.message_texts import info_text
from src.bot.structures.keyboards import DEVINFO_BOARD

info_router = Router(name='info')


@info_router.message(Command(commands=['info']))
@info_router.message(F.text == 'ℹ️ Info')
async def help_handler(message: types.Message):
    return await message.answer(info_text, reply_markup=DEVINFO_BOARD, parse_mode='HTML')
