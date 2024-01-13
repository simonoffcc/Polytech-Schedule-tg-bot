from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.utils.markdown import hbold

from src.app import texts as BotText
from src.app import parser_methods as Schedule
from src.app import keyboards as kb

main_router = Router(name='main')

# todo: Добавить машину состояний на этапах выбора института и номера группы


@main_router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    acronyms_list = Schedule.get_institutes_acronyms()
    keyboard = await kb.generate_acronyms_reply_keyboard(acronyms_list)
    await message.answer(BotText.institute_unknownUser.format(hbold(message.from_user.full_name)),
                         reply_markup=keyboard)


@main_router.message(Command(commands='today_tomorrow'))
async def today_tomorrow_schedule_handler(message: types.Message) -> None:
    week_schedule = "Пока ничего нет!"
    await message.answer(BotText.currentWeek_schedule.format(week_schedule), reply_markup=kb.main_menu)


@main_router.message()
async def unknown_message_handler(message: types.Message) -> None:
    await message.answer(f'Привет, {hbold(message.from_user.full_name)}!', reply_markup=kb.main_menu)
