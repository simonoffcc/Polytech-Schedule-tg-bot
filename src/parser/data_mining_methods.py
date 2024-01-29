import json
import asyncio
from datetime import datetime
from typing import Union

from src.parser.parsing_methods import (_parse_institute_selection_page,
                                        _parse_group_selection_page,
                                        _parse_week_schedule)


async def get_institutes_data() -> list[dict]:
    data = await _parse_institute_selection_page()
    institutes_data = data['faculties']['data']
    if not isinstance(institutes_data, list):
        raise TypeError("Ошибка хранения информации об институтах в формате 'list[dict, ...]'!")
    return institutes_data


async def get_groups_data(institute_id: int) -> list[dict]:
    data = await _parse_group_selection_page(institute_id)
    groups_data = data['groups']['data'][f'{institute_id}']
    if not isinstance(groups_data, list):
        raise TypeError("Ошибка хранения информации о группах в формате 'list[dict,...]'!")
    return groups_data


async def get_institutes_ids() -> list[int]:
    faculties = await get_institutes_data()
    institutes_ids = list(filter(None, (faculty.get('id') for faculty in faculties)))
    return institutes_ids


async def get_institutes_abbrs() -> list[str]:
    faculties = await get_institutes_data()
    institutes_abbrs = list(filter(None, (faculty.get('abbr') for faculty in faculties)))
    return institutes_abbrs


async def get_value_by_another_key(key_to_search: str,
                                   value_to_search: str | int,
                                   key_to_return_value: str) -> int | str | None:
    """
    Универсальный метод, который позволяет получить информацию из списка словарей по заданному ключу,
    в котором содержится переданное значение, относящееся к другому ключу.

    :param key_to_search: Ключ, по которому искать
    :param value_to_search: Значение, по которому найти словарь в списке
    :param key_to_return_value: Ключ, по которому вернуть значение из найденного словаря
    """
    faculties = await get_institutes_data()
    for faculty in faculties:
        if faculty.get(key_to_search) == value_to_search:
            return faculty.get(key_to_return_value)
    return


async def get_institutes_names() -> list[str]:
    faculties = await get_institutes_data()
    institutes_names = list(filter(None, (faculty.get('name') for faculty in faculties)))
    return institutes_names


async def get_today_schedule_str(faculty_id: int, group_id: int) -> str:
    ...


async def get_tomorrow_schedule_str(faculty_id: int, group_id: int) -> str:
    # get_today_schedule_str(date=.now+next_day)
    ...


async def get_one_day_schedule_str(faculty_id: int, group_id: int,
                                   key: str = None,
                                   date: Union[datetime, str] = None) -> str:
    ...


async def get_week_schedule_str(faculty_id: int, group_id: int,
                                date: Union[datetime, str]) -> str:
    # todo: метод сам по себе плохой, ибо если на всей недели расписание,
    #  то сообщение будет очень большим и нечитаемым.
    #  Поэтому нужно стремиться к решению, как здесь: https://t.me/misis_sch_bot
    data = await _parse_week_schedule(faculty_id=faculty_id, group_id=group_id, date=date)
    weekdays_data = data['lessons']['data'][f'{group_id}']  # list[dict] - every weekday info
    if not isinstance(weekdays_data, list):
        raise TypeError("Ошибка хранения информации о расписании в формате 'list[dict,...]'!")
    generated_string = []
    for weekday in weekdays_data:
        each_day = ''
        date_object = datetime.strptime(weekday['date'], '%Y-%m-%d')
        date_and_month = date_object.strftime('%d %b.')
        day_of_week = date_object.strftime('%a')
        each_day += f'{date_and_month}, {day_of_week.lower()}\n'
        for lesson in weekday['lessons']:
            each_day += f"{lesson['time_start']}-{lesson['time_end']}\n"
            each_day += f"{lesson['subject']}\n"
            each_day += f"{lesson['typeObj']['name']}\n"
            each_day += f"{', '.join([group['name'] for group in lesson['groups']])}\n"
            if lesson['teachers']:
                each_day += f"{', '.join([teacher['full_name'] for teacher in lesson['teachers']])}\n"
            if lesson['lms_url']:
                each_day += f"{lesson['lms_url']}\n"
            each_day += f"{lesson['auditories'][0]['building']['name']}, ауд. {lesson['auditories'][0]['name']}\n"
        generated_string.append(each_day)

    return '\n'.join(generated_string)


async def _show_schedule_data_temp(faculty_id: int = 125, group_id: int = 38645, date: str = '2025-01-21'):
    data = await _parse_week_schedule(faculty_id=faculty_id, group_id=group_id, date=date)
    weekdays_data = data['lessons']['data'][f'{group_id}']  # list[dict] - every weekday info
    if not isinstance(weekdays_data, list):
        raise TypeError("Ошибка хранения информации о расписании в формате 'list[dict,...]'!")
    if not weekdays_data:
        print("Нет пар!")
    else:
        print(json.dumps(weekdays_data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    asyncio.run(_show_schedule_data_temp())
    week_schedule: str = asyncio.run(get_today_schedule_str(125, 38645))
    print(week_schedule)


institutes_acronyms: list[str] = asyncio.run(get_institutes_abbrs())
