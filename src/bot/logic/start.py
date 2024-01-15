from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

# from src.bot.filters.register_filter import RegisterFilter
from src.bot.middlewares import RegisterMiddleware

from src.bot.structures.message_texts import hi, help_text
from src.bot.structures.keyboards import MENU_BOARD

start_router = Router(name='start')
start_router.message.middleware(RegisterMiddleware())


@start_router.message(CommandStart())
@start_router.message(F.text.lower() == 'начать')
async def start_handler(message: types.Message):
    await message.answer(hi.format(hbold(message.from_user.full_name)), parse_mode='HTML')
    return await message.answer(help_text, parse_mode='HTML', reply_markup=MENU_BOARD)
