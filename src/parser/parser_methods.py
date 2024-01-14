import re
import json
import requests


URL = 'https://ruz.spbstu.ru/'


class DataNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


def parse_institute_selection_page() -> dict:
    req = requests.get(URL)
    html_text = req.text
    data = re.search(r'window.__INITIAL_STATE__ = ({.+});', html_text)
    if not data:
        raise DataNotFound("Информация об институтах из 'window.__INITIAL_STATE__' не найдена!")
    data = json.loads(data.group(1))
    return data


def parse_group_selection_page(institute_id: int) -> dict:
    url = f'https://ruz.spbstu.ru/faculty/{institute_id}/groups/'
    req = requests.get(url)
    html_text = req.text
    data = re.search(r'window.__INITIAL_STATE__ = ({.+});', html_text)
    if not data:
        raise DataNotFound("Информация о группах из 'window.__INITIAL_STATE__' не найдена!")
    data = json.loads(data.group(1))
    return data


def get_institutes_data() -> list[dict, ...]:
    data = parse_institute_selection_page()
    institutes_data = data['faculties']['data']
    if not isinstance(institutes_data, list):
        raise TypeError("Ошибка хранения информации об институтах в формате 'list[dict, ...]'!")
    return institutes_data


def get_groups_data(institute_id: int) -> list[dict, ...]:
    data = parse_group_selection_page(institute_id)
    groups_data = data['groups']['data']
    if not isinstance(groups_data, list):
        raise TypeError("Ошибка хранения информации о группах в формате 'list[dict,...]'!")
    return groups_data


def get_institutes_ids() -> list[int]:
    faculties = get_institutes_data()
    institutes_ids = list(filter(None, (faculty.get('id') for faculty in faculties)))
    return institutes_ids


def get_institutes_names() -> list[str]:
    faculties = get_institutes_data()
    institutes_names = list(filter(None, (faculty.get('name') for faculty in faculties)))
    return institutes_names


def get_institutes_acronyms() -> list[str]:
    faculties = get_institutes_data()
    institutes_abbrs = list(filter(None, (faculty.get('abbr') for faculty in faculties)))
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
    faculties = get_institutes_data()
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
    faculties_data: list[dict] = get_institutes_data()
    institutes_abbrs: list[str] = get_institutes_acronyms()


parser = ScheduleData()

# todo: Написать функцию, которая будет парсить инфромацию со страницы институтов и сохранять в json-файл
# todo: Написать функцию, которая будет парсить инфромацию со всех страниц институтов с группами (16 страниц)
#  и сохранять в отдельные json-файлы

