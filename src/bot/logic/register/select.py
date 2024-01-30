from aiogram import types, F
from aiogram.filters import CommandStart, StateFilter, and_f, or_f
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext

from .router import register_router
from src.db import Database
from src.bot.filters import (RegisterFilter, IsInstituteExists, CorrectGroupFormat, IsGroupExists)
from src.bot.structures.lexicon import (hi, choose_institute, choose_group,
                                        dont_know_institute, enter_valid_institute,
                                        not_found_group, enter_valid_group,
                                        schedule_is_set, cancel_registration)
from src.bot.structures.keyboards import (generate_acronyms_reply_keyboard, MENU_BOARD,
                                          BACK_OR_CANCEL, CONFIRMATION_BOARD)
from src.bot.structures.states import Registration


@register_router.message(and_f(F.text.lower().in_(["отмена", "отменить настройку"]),
                               or_f(Registration.institute_choice,
                                    Registration.group_choice,
                                    Registration.confirmation)))
async def cancel_button_handler(message: types.Message, state: FSMContext):
    await state.clear()
    return await message.answer(cancel_registration, reply_markup=MENU_BOARD)


@register_router.message(and_f(Registration.group_choice, F.text.lower() == "назад"))
async def back_button_handler(message: types.Message, state: FSMContext):
    await state.set_state(Registration.institute_choice)
    faculties = await generate_acronyms_reply_keyboard()
    return await message.answer(choose_institute, reply_markup=faculties)


@register_router.message(and_f(Registration.confirmation, F.text.lower() == "назад"))
async def add_user_handler(message: types.Message, state: FSMContext):
    await state.set_state(Registration.group_choice)
    register_data = await state.get_data()
    await message.answer(f"Выбран институт: {register_data['institute']}", reply_markup=BACK_OR_CANCEL)
    return await message.answer(choose_group)


@register_router.message(and_f(StateFilter(None),
                               ~RegisterFilter(),
                               or_f(F.text.lower() == 'начать', CommandStart())))
async def start_reg_user_handler(message: types.Message, state: FSMContext):
    await state.set_state(Registration.institute_choice)
    await message.answer(hi.format(hbold(message.from_user.full_name)), parse_mode='HTML')
    faculties = await generate_acronyms_reply_keyboard()
    return await message.answer(choose_institute, reply_markup=faculties)


@register_router.message(and_f(Registration.institute_choice, IsInstituteExists()))
async def choose_institute_handler(message: types.Message, state: FSMContext):
    await state.update_data(institute=message.text)
    await state.set_state(Registration.group_choice)
    await message.answer(f'Выбран институт: {message.text}', reply_markup=BACK_OR_CANCEL)
    return await message.answer(choose_group)


@register_router.message(and_f(Registration.institute_choice, ~IsInstituteExists()))
async def unknown_institute_handler(message: types.Message):
    faculties = await generate_acronyms_reply_keyboard()
    await message.answer(dont_know_institute, reply_markup=faculties)
    return await message.answer(enter_valid_institute, reply_markup=faculties)


@register_router.message(and_f(Registration.group_choice, ~CorrectGroupFormat()))
async def incorrect_group_handler(message: types.Message):
    return await message.answer(enter_valid_group)


@register_router.message(and_f(Registration.group_choice, ~IsGroupExists()))
async def not_found_group_handler(message: types.Message):
    return await message.answer(not_found_group)


@register_router.message(and_f(Registration.group_choice,
                               CorrectGroupFormat(),
                               IsGroupExists()))
async def data_confirmation_handler(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    register_data = await state.get_data()
    await message.answer(f"Выбран институт: {register_data['institute']}.\n"
                         f"Выбрана группа: {register_data['group']}.")
    await state.set_state(Registration.confirmation)
    return await message.answer("Всё верно?", reply_markup=CONFIRMATION_BOARD)


@register_router.message(and_f(Registration.confirmation, F.text.lower() == "да"))
async def add_user_handler(message: types.Message, state: FSMContext, **kwargs):
    register_data = await state.get_data()
    db: Database = kwargs.get('db')
    await db.user.new(
        user_id=message.from_user.id,
        user_name=message.from_user.full_name,
        institute_id=125,               # todo: get_key_by_another_value(register_data['institute'])
        group_id=38574,                 # todo: get_key_by_another_value(register_data['group'])
        institute_abbr=register_data['institute'],
        group_name=register_data['group']
    )
    await state.clear()
    return await message.answer(schedule_is_set, reply_markup=MENU_BOARD)


@register_router.message(Registration.confirmation)
async def unknown_confirmation_message_handler(message: types.Message, state: FSMContext):
    register_data = await state.get_data()
    await message.answer(f"Выбран институт: {register_data['institute']}.\n"
                         f"Выбрана группа: {register_data['group']}.")
    await state.set_state(Registration.confirmation)
    return await message.answer("Всё верно?", reply_markup=CONFIRMATION_BOARD)
