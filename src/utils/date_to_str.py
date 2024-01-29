from typing import Union
from datetime import datetime


async def date_to_str(date: Union[datetime, str] = None) -> str:
    if date is None:
        date = datetime.now()
    elif isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')

    if not isinstance(date, datetime):
        raise ValueError("Input should be either a string or a datetime object")

    return date.strftime('%Y-%m-%d')
