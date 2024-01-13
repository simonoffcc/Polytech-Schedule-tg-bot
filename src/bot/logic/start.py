from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from src.parser import get_institutes_acronyms

from src.bot.structures.texts import today_schedule, hi, choose_institute
from src.bot.structures.keyboards import generate_acronyms_reply_keyboard
from src.bot.structures.keyboards import MENU_BOARD

start_router = Router(name='start')


# todo: Если юзера НЕТ в базе
@start_router.message(CommandStart())
@start_router.message(F.text.lower() == 'начать')
async def start_handler_user_not_exists(message: types.Message):
    """Если пользователя нет в базе, то отправляем клавиатуру для выбора института."""
    institutes = await get_institutes_acronyms()
    faculties = await generate_acronyms_reply_keyboard(institutes)
    await message.answer(hi.format(hbold(message.from_user.full_name)), parse_mode='HTML')
    await message.answer(choose_institute, reply_markup=faculties, parse_mode='HTML')


# todo: Если юзера ЕСТЬ в базе
@start_router.message(CommandStart())
@start_router.message(F.text.lower() == 'начать')
async def start_handler(message: types.Message):
    """Если пользователь уже есть в базе, то просто отправляем расписание на сегодня."""
    return await message.answer(today_schedule.format('<TODAY_SCHEDULE>'),
                                reply_markup=MENU_BOARD)
