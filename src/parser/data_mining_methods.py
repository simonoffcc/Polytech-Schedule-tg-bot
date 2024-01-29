import json
import asyncio
from datetime import datetime
from typing import Union

from src.parser.parsing_methods import (_parse_institute_selection_page,
                                        _parse_group_selection_page,
                                        _parse_week_schedule)

# todo: Почти каждый метод, который не обращается к конкретному расписанию,
#  при вызове делает html-запросы на страницу с информацией об институтах и информации о группах
#  для получения соответствующих данных.
#  Предполагаю, что это не очень рационально, поэтому в этом пакете есть файл updating_data.py,
#  который предположительно нужно использовать как отдельно запущенный сервис,
#  и будет один раз в единицу времени (например, полгода) обновлять необходимые данные.
#  А в методах ниже изменить логику постоянного парсинга на чтение данных из файла


async def get_institutes_data() -> list[dict]:
    data = await _parse_institute_selection_page()
    institutes_data = data['faculties']['data']
    if not isinstance(institutes_data, list):
        raise TypeError("Ошибка хранения информации об институтах в формате 'list[dict]'!")
    return institutes_data


async def get_groups_data(institute_id: int) -> list[dict]:
    data = await _parse_group_selection_page(institute_id)
    groups_data = data['groups']['data'][f'{institute_id}']
    if not isinstance(groups_data, list):
        raise TypeError("Ошибка хранения информации о группах в формате 'list[dict]'!")
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


async def get_week_schedule_data(faculty_id: int, group_id: int,
                                 date: Union[datetime, str]) -> list[dict]:
    """Возвращает список словарей, каждый из которых представляет информацию об 1-ом дне недели.
    Служит проводником между методом парсера расписания на заданную неделю* и методами, которые превращают эти сырые
    данные в текст, валидный для чтения человеком.

    * - заданной неделей считается неделя, которая содержит переданную в метод дату (воскресенье тоже поддерживается).
    """
    data = await _parse_week_schedule(faculty_id=faculty_id, group_id=group_id, date=date)
    weekdays_data = data['lessons']['data'][f'{group_id}']  # list[dict] - every weekday info
    if not isinstance(weekdays_data, list):
        raise TypeError("Ошибка хранения информации о расписании в формате 'list[dict]'!")
    return weekdays_data


async def _temp_print_schedule_data(faculty_id: int = 125, group_id: int = 38645, date: str = '2023-11-23'):
    data = await _parse_week_schedule(faculty_id=faculty_id, group_id=group_id, date=date)
    weekdays_data = data['lessons']['data'][f'{group_id}']  # list[dict] - every weekday info
    if not isinstance(weekdays_data, list):
        raise TypeError("Ошибка хранения информации о расписании в формате 'list[dict]'!")
    if not weekdays_data:
        print("Нет пар!")
    else:
        print(json.dumps(weekdays_data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    asyncio.run(_temp_print_schedule_data())

institutes_acronyms: list[str] = asyncio.run(get_institutes_abbrs())
