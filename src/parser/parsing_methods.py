import re
import json
import requests
from datetime import datetime


BASE_URL = 'https://ruz.spbstu.ru/'
GROUPS_URL = 'https://ruz.spbstu.ru/faculty/{0}/groups/'
PERSONALIZED_URL = 'https://ruz.spbstu.ru/faculty/{0}}/groups/{1}?date={2}'  # YYYY-MM-DD


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


"""
def parse_today_schedule(user) -> str:
    ...


def parse_tomorrow_schedule(user) -> str:
    ...


def parse_next_week_schedule(user) -> str:
    ...
"""


async def _parse_current_week_schedule(faculty_id: int, group_id: int) -> dict:
    """Функция, которая парсит расписание на текущую неделю"""
    url = PERSONALIZED_URL.format(faculty_id, group_id, datetime.now().strftime('%Y-%m-%d'))
    req = requests.get(url)
    if req.status_code != 200:
        raise ValueError(f"Ошибка при запросе по ссылке ({url}): {req.status_code}")
    html_text = req.text
    data = re.search(r'window.__INITIAL_STATE__ = ({.+});', html_text)
    if not data:
        raise DataNotFound("Данные о расписании из 'window.__INITIAL_STATE__' не найдены!")
    data = json.loads(data.group(1))
    return data
