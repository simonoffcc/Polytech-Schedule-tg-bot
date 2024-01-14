from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from src.bot.structures.texts import hi

start_router = Router(name='start')


@start_router.message(CommandStart())
@start_router.message(F.text.lower() == 'начать')
async def start_handler(message: types.Message):
    return await message.answer(hi.format(hbold(message.from_user.full_name)), parse_mode='HTML')
