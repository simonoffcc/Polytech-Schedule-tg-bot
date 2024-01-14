from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from src.bot.structures.keyboards import MENU_BOARD
from src.bot.structures.message_texts import hi, command_start

start_router = Router(name='start')


@start_router.message(CommandStart())
@start_router.message(F.text.lower() == 'начать')
async def start_handler(message: types.Message):
    await message.answer(hi.format(hbold(message.from_user.full_name)), parse_mode='HTML')
    await message.answer(command_start, reply_markup=MENU_BOARD, parse_mode='MARKDOWN_V2')
