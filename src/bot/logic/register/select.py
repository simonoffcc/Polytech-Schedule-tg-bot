from aiogram import types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext

from src.bot.filters import CorrectGroupFormat, RegisterFilter
from src.db import Database
from .router import register_router
from src.bot.structures.message_texts import (hi, choose_institute, choose_group,
                                              try_again_choose_institute, try_again_choose_group,
                                              try_valid_value_choose_group,
                                              schedule_is_set)
from src.parser import parser
from src.bot.structures.keyboards import generate_acronyms_reply_keyboard
from src.bot.structures.keyboards import MENU_BOARD

from src.bot.structures.states import Registration


@register_router.message(StateFilter(None), CommandStart(), ~RegisterFilter())
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
async def choose_institute_handler(message: types.Message, state: FSMContext, **kwargs):
    await state.update_data(group_num=message.text)
    reg = await state.get_data()
    db: Database = kwargs.get('db')
    await db.user.new(
        user_id=message.from_user.id,
        user_name=message.from_user.full_name,
        institute_id=100,               # todo: get_key_by_another_value(reg['institute'])
        group_id=38574,                 # todo: get_key_by_another_value(reg['group_num'])
        institute_abbr=reg['institute'],
        group_name=reg['group_num']
    )
    await message.answer(f"Выбран институт: {reg['institute']}.\n"
                         f"Выбрана группа: {reg['group_num']}.")
    await state.clear()
    return await message.answer(schedule_is_set, reply_markup=MENU_BOARD)


@register_router.message(Registration.choosing_group_number, ~CorrectGroupFormat())
async def choose_institute_handler(message: types.Message):
    return await message.answer(try_valid_value_choose_group)
