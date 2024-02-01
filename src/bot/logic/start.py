from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from src.bot.filters import RegisterFilter
from src.bot.structures.lexicon import hi, help_text
from src.bot.structures.keyboards import MENU_BOARD

start_router = Router(name='start')
start_router.message.filter(RegisterFilter())


@start_router.message(CommandStart())
@start_router.message(F.text.lower() == 'начать')
async def start_handler(message: types.Message, state: FSMContext):
    # todo: решить проблему с секурити формат строк
    await message.answer(hi.format(name=hbold(message.from_user.full_name)), parse_mode='HTML')
    await state.clear()
    return await message.answer(help_text, parse_mode='HTML', reply_markup=MENU_BOARD)
