import re
import json
from typing import Union

import requests
from datetime import datetime


BASE_URL = 'https://ruz.spbstu.ru/'
GROUPS_URL = 'https://ruz.spbstu.ru/faculty/{0}/groups/'
PERSONALIZED_URL = 'https://ruz.spbstu.ru/faculty/{0}/groups/{1}?date={2}'  # YYYY-MM-DD


class DataNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


async def _parse_institute_selection_page() -> dict:
    url = BASE_URL
    req = requests.get(url)
    if req.status_code != 200:
        raise ValueError(f"Ошибка при запросе по ссылке ({url}): {req.status_code}")
    html_text = req.text
    data = re.search(r'window.__INITIAL_STATE__ = ({.+});', html_text)
    if not data:
        raise DataNotFound("Данные об институтах из 'window.__INITIAL_STATE__' не найдены!")
    data = json.loads(data.group(1))
    return data


async def _parse_group_selection_page(institute_id: int) -> dict:
    url = GROUPS_URL.format(institute_id)
    req = requests.get(url)
    if req.status_code != 200:
        raise ValueError(f"Ошибка при запросе по ссылке ({url}): {req.status_code}")
    html_text = req.text
    data = re.search(r'window.__INITIAL_STATE__ = ({.+});', html_text)
    if not data:
        raise DataNotFound("Данные о группах из 'window.__INITIAL_STATE__' не найдены!")
    data = json.loads(data.group(1))
    return data


async def date_to_str(date: Union[datetime, str] = None) -> str:
    if date is None:
        date = datetime.now()
    elif isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')

    if not isinstance(date, datetime):
        raise ValueError("Input should be either a string or a datetime object")

    return date.strftime('%Y-%m-%d')


async def _parse_week_schedule(faculty_id: int, group_id: int, date: Union[datetime, str] = None) -> dict:
    """Функция, которая парсит расписание на всю неделю, в которой содержится указанная дата."""
    date = await date_to_str(date)
    url = PERSONALIZED_URL.format(faculty_id, group_id, date)
    req = requests.get(url)
    if req.status_code != 200:
        raise ValueError(f"Ошибка при запросе по ссылке ({url}): {req.status_code}")
    html_text = req.text
    data = re.search(r'window.__INITIAL_STATE__ = ({.+});', html_text)
    if not data:
        raise DataNotFound("Данные о расписании из 'window.__INITIAL_STATE__' не найдены!")
    data = json.loads(data.group(1))
    return data


"""
async def _parse_today_schedule(user) -> str:
    ...


async def _parse_tomorrow_schedule(user) -> str:
    ...


async def _parse_next_week_schedule(user) -> str:
    ...
"""
