from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext

from src.bot.filters import CorrectGroupFormat
from .router import register_router
from src.bot.structures.message_texts import (hi, choose_institute, choose_group,
                                              try_again_choose_institute, try_again_choose_group,
                                              registration_completed)
from src.parser import parser
from src.bot.structures.keyboards import generate_acronyms_reply_keyboard
from src.bot.structures.keyboards import MENU_BOARD

from src.bot.structures.states import Registration


@register_router.message(CommandStart())
@register_router.message(F.text.lower() == 'начать')
async def start_unknown_user_handler(message: types.Message, state: FSMContext):
    await state.set_state(Registration.choosing_institute)
    await message.answer(hi.format(hbold(message.from_user.full_name)), parse_mode='HTML')
    faculties = generate_acronyms_reply_keyboard(parser.institutes_abbrs)
    return await message.answer(choose_institute, reply_markup=faculties)


@register_router.message(Registration.choosing_institute, F.text.in_(parser.institutes_abbrs))
async def choose_institute_handler(message: types.Message, state: FSMContext):
    await state.update_data(institute=message.text)
    await state.set_state(Registration.choosing_group_number)
    await message.answer(f'Выбран институт: {message.text}', reply_markup=ReplyKeyboardRemove())
    return await message.answer(choose_group)


@register_router.message(Registration.choosing_institute)
async def unknown_institute_handler(message: types.Message):
    faculties = generate_acronyms_reply_keyboard(parser.institutes_abbrs)
    return await message.answer(try_again_choose_institute, reply_markup=faculties)


@register_router.message(Registration.choosing_group_number, CorrectGroupFormat())
async def choose_institute_handler(message: types.Message, state: FSMContext):
    await state.update_data(group_num=message.text)
    # todo: если страница существует, добавляем пользователя в базу
    await state.clear()
    await message.answer(f'Выбран номер группы: {message.text}')
    return await message.answer(registration_completed, reply_markup=MENU_BOARD)


@register_router.message(Registration.choosing_group_number, ~CorrectGroupFormat())
async def choose_institute_handler(message: types.Message):
    return await message.answer(try_again_choose_group)
