import json
import asyncio
from datetime import datetime, timedelta
from typing import Union

from src.parser.data_mining_methods import get_week_schedule_data


async def turn_day_to_str(day_data: dict) -> str:
    day_str = ''
    date_object = datetime.strptime(day_data['date'], '%Y-%m-%d')
    date_and_month = date_object.strftime('%d %b')
    day_of_week = date_object.strftime('%a')
    day_str += f'{date_and_month}, {day_of_week.lower()}\n'
    for lesson in day_data['lessons']:
        day_str += f"{lesson['time_start']}-{lesson['time_end']}\n"
        day_str += f"{lesson['subject']}\n"
        if lesson['typeObj']['name']:
            day_str += f"{lesson['typeObj']['name']}\n"
        # todo: переделать логику, ибо большое кол-во групп захламляет оформление сообщения.
        #  При этом, информация об этих группах может быть полезной.
        # day_str += f"{', '.join([group['name'] for group in lesson['groups']])}\n"
        if lesson['teachers']:
            day_str += f"{', '.join([teacher['full_name'] for teacher in lesson['teachers']])}\n"
        if lesson['lms_url']:
            day_str += f"{lesson['lms_url']}\n"
        day_str += f"{lesson['auditories'][0]['building']['name']}, ауд. {lesson['auditories'][0]['name']}\n"
    return day_str


async def get_week_schedule_str(faculty_id: int, group_id: int,
                                date: Union[datetime, str] = None) -> str:
    # todo: метод сам по себе плохой, ибо если на всей недели расписание,
    #  то сообщение будет очень большим и нечитаемым.
    #  Поэтому нужно стремиться к решению, как здесь: https://t.me/misis_sch_bot
    #  (с инлайн-клавиатурой - на каждый день или со стрелками для перелистывания)
    weekdays_data = await get_week_schedule_data(faculty_id=faculty_id, group_id=group_id, date=date)
    generated_string = []
    for weekday in weekdays_data:
        # todo: заполнить дни без пар текстом "Пар не запланировано."
        # todo: решить проблему с разметкой и пробелами между предметами
        generated_string.append(await turn_day_to_str(weekday))
    return '\n'.join(generated_string)


async def get_today_schedule_str(faculty_id: int, group_id: int) -> str:
    today_date = datetime.now().strftime('%Y-%m-%d')
    weekdays_data = await get_week_schedule_data(faculty_id=faculty_id, group_id=group_id, date=today_date)
    today_data = None
    for weekday in weekdays_data:
        if weekday['date'] == today_date:
            today_data = weekday
            break
    if not today_data or today_data is None:
        date_object = datetime.strptime(today_date, '%Y-%m-%d')
        date_and_month = date_object.strftime('%d %b')
        day_of_week = date_object.strftime('%a')
        return f"{date_and_month}, {day_of_week.lower()}\nПар не запланировано.\n"

    result = await turn_day_to_str(today_data)
    return result


async def get_tomorrow_schedule_str(faculty_id: int, group_id: int) -> str:
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_date = tomorrow.strftime("%Y-%m-%d")
    weekdays_data = await get_week_schedule_data(faculty_id=faculty_id, group_id=group_id, date=tomorrow_date)
    today_data = None
    for weekday in weekdays_data:
        if weekday['date'] == tomorrow_date:
            today_data = weekday
            break
    if not today_data or today_data is None:
        date_object = datetime.strptime(tomorrow_date, '%Y-%m-%d')
        date_and_month = date_object.strftime('%d %b')
        day_of_week = date_object.strftime('%a')
        return f"{date_and_month}, {day_of_week.lower()}\nПар не запланировано."
    result = await turn_day_to_str(today_data)
    return result


async def get_particular_day_schedule(faculty_id: int, group_id: int,
                                      key: str = None,
                                      date: Union[datetime, str] = None) -> str:
    ...


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, "")
    print(asyncio.run(get_today_schedule_str(125, 38645)))
    print(asyncio.run(get_tomorrow_schedule_str(125, 38645)))
