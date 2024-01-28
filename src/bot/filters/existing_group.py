from aiogram.types import Message
from aiogram.filters import BaseFilter


class IsGroupExists(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        result: bool = ...  # todo: Существует ли группа (смотреть src.parser.data_mining_methods.py)
        return result
