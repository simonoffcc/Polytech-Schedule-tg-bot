from aiogram import Router, types, F
from aiogram.filters import Command

from src.bot.structures.lexicon import (today_tomorrow_schedule,
                                        current_week_schedule,
                                        next_week_schedule)
from src.bot.structures.keyboards import MENU_BOARD
from src.parser import get_week_schedule_str, get_day_schedule_by_key_str

schedule_router = Router(name='schedule')


@schedule_router.message(Command(commands=['today_tomorrow']))
@schedule_router.message(F.text == 'Сегодня и завтра')
async def today_tomorrow_command_handler(message: types.Message):
    return await message.answer(
        today_tomorrow_schedule.format(
            await get_day_schedule_by_key_str(125, 38645, key=0),
            await get_day_schedule_by_key_str(125, 38645, key=1)),
        reply_markup=MENU_BOARD)


@schedule_router.message(Command(commands=['week']))
@schedule_router.message(F.text == 'Текущая неделя')
async def week_command_handler(message: types.Message):
    return await message.answer(
        current_week_schedule.format(
            await get_week_schedule_str(125, 38645)),
        reply_markup=MENU_BOARD)


@schedule_router.message(Command(commands=['next_week']))
@schedule_router.message(F.text == 'Следующая неделя')
async def next_week_command_handler(message: types.Message):
    return await message.answer(
        next_week_schedule.format('<NEXT WEEK SCHEDULE>'),
                                reply_markup=MENU_BOARD)
