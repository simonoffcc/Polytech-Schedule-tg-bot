import re
import json
import requests


class FacultiesNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


def parse_institute_selection_page() -> dict:
    URL = 'https://ruz.spbstu.ru/'
    req = requests.get(URL)
    html_text = req.text
    data = re.search(r'window.__INITIAL_STATE__ = ({.+});', html_text)
    if not data:
        raise FacultiesNotFound("Информация об институтах из 'window.__INITIAL_STATE__' не найдена!")
    data = json.loads(data.group(1))
    return data


def get_faculties_data() -> list[dict, ...]:
    data = parse_institute_selection_page()
    faculties_data = data['faculties']['data']
    if not isinstance(faculties_data, list):
        raise FacultiesNotFound("Ошибка хранения информации об институтах в формате 'list[dict, ...]'!")
    return faculties_data


def get_institutes_ids() -> list[int]:
    faculties = get_faculties_data()
    values = [faculty.get('id') for faculty in faculties]
    institutes_ids = [value for value in values if value is not None]
    return institutes_ids


def get_institutes_names() -> list[str]:
    faculties = get_faculties_data()
    values = [faculty.get('name') for faculty in faculties]
    institutes_names = [value for value in values if value is not None]
    return institutes_names


def get_institutes_acronyms() -> list[str]:
    faculties = get_faculties_data()
    values = [faculty.get('abbr') for faculty in faculties]
    institutes_abbrs = [value for value in values if value is not None]
    return institutes_abbrs


async def get_value_by_another_key(*,
                                   key_to_search: str,
                                   value_to_search: str | int,
                                   key_to_return_value: str) -> int | str:
    """
    Метод, который позволяет получить информацию из списка словарей по заданному ключу,
    в котором содержится переданное значение, относящееся к другому ключу.

    :param key_to_search: Ключ, по которому искать
    :param value_to_search: Значение, по которому найти словарь в списке
    :param key_to_return_value: Ключ, по которому вернуть значение из найденного словаря
    """
    faculties = get_faculties_data()
    for faculty in faculties:
        if faculty.get(key_to_search) == value_to_search:
            return faculty.get(key_to_return_value)

"""
async def parse_today_schedule(user: User) -> str:
    ...


async def parse_tomorrow_schedule(user: User) -> str:
    ...


async def parse_current_week_schedule(user: User) -> str:
    ...


async def parse_next_week_schedule(user: User) -> str:
    ...
"""

"""
def functional_example():
    data_dict = parse_institute_selection_page()
    faculties_list = get_faculties_data(data_dict)
    
    keyboard = get_institutes_acronyms(faculties_list)
    # message.send(..., keyboard=keyboard)
    
    user_message_from_keyboard = "ИКНТ"
    result = find_and_get_value(faculties_list, 'abbr', user_message_from_keyboard, 'id')
    print(result)
    result = find_and_get_value(faculties_list, 'abbr', user_message_from_keyboard, 'name')
    print(result)
"""


class ScheduleData:
    faculties_data: list[dict] = get_faculties_data()
    institutes_abbrs: list[str] = get_institutes_acronyms()


parser = ScheduleData()
