from aiogram.types import Message
from aiogram.filters import BaseFilter

from src.parser import institutes_acronyms


class IsInstituteExists(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        result: bool = message.text in institutes_acronyms
        return result
        # todo: Здесь можно добавить проверку на институты типа "ИКНТ"
        # todo: (в базе расписания и при парсинге он есть, а по факту его нет)
