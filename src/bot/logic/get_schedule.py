from aiogram import Router, types, F
from aiogram.filters import Command

from src.bot.structures.message_texts import (today_tomorrow_schedule,
                                              current_week_schedule,
                                              next_week_schedule)
from src.bot.structures.keyboards import MENU_BOARD
from src.parser import get_week_schedule_str

get_schedule_router = Router(name='schedule')


@get_schedule_router.message(Command(commands=['today_tomorrow']))
@get_schedule_router.message(F.text == 'Сегодня и завтра')
async def today_tomorrow_command_handler(message: types.Message):
    return await message.answer(today_tomorrow_schedule.format('<TODAY SCHEDULE>', '<TOMORROW SCHEDULE>'),
                                reply_markup=MENU_BOARD)


@get_schedule_router.message(Command(commands=['week']))
@get_schedule_router.message(F.text == 'Текущая неделя')
async def week_command_handler(message: types.Message):
    string = await get_week_schedule_str(125, 38645, '2023-11-27')
    return await message.answer(current_week_schedule.format(string),
                                reply_markup=MENU_BOARD)


@get_schedule_router.message(Command(commands=['next_week']))
@get_schedule_router.message(F.text == 'Следующая неделя')
async def next_week_command_handler(message: types.Message):
    return await message.answer(next_week_schedule.format('<NEXT WEEK SCHEDULE>'),
                                reply_markup=MENU_BOARD)
