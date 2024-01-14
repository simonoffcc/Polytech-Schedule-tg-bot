from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext

from .router import register_router
from src.parser import parser
from src.bot.structures.message_texts import (hi, choose_institute, choose_group,
                                              try_again_choose_institute, try_again_choose_group,
                                              registration_completed)
from src.bot.structures.keyboards import generate_acronyms_reply_keyboard
from src.bot.structures.keyboards import MENU_BOARD

from src.bot.structures.states import Registration


@register_router.message(CommandStart())
# @register_router.message(F.text.lower() == 'начать')
async def start_unknown_user_handler(message: types.Message, state: FSMContext):
    faculties = generate_acronyms_reply_keyboard(parser.institutes_abbrs)
    await message.answer(hi.format(hbold(message.from_user.full_name)), parse_mode='HTML')
    await message.answer(choose_institute, reply_markup=faculties)
    await state.set_state(Registration.choosing_institute)


@register_router.message(Registration.choosing_institute, F.text.in_(parser.institutes_abbrs))
async def choose_institute_handler(message: types.Message, state: FSMContext):
    await state.update_data(institute=message.text)
    await message.answer(f'Выбран институт: {message.text}', reply_markup=ReplyKeyboardRemove())
    await message.answer(choose_group)
    await state.set_state(Registration.choosing_group_number)


@register_router.message(Registration.choosing_institute)
async def unknown_institute_handler(message: types.Message):
    faculties = generate_acronyms_reply_keyboard(parser.institutes_abbrs)
    await message.answer(try_again_choose_institute, reply_markup=faculties)


@register_router.message(Registration.choosing_group_number)  # todo: свой фильтр на корректность ввода группы
async def choose_institute_handler(message: types.Message, state: FSMContext):
    await state.update_data(group_num=message.text)
    await message.answer(f'Выбран номер группы: {message.text}')
    await message.answer(registration_completed,
                         reply_markup=MENU_BOARD)
    await state.clear()


@register_router.message(Registration.choosing_group_number)
async def choose_institute_handler(message: types.Message):
    await message.answer(try_again_choose_group)
