import re
from aiogram.types import Message
from aiogram.filters import BaseFilter


class CorrectGroupFormat(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        pattern = re.compile(r'^.{1,10}/.{1,10}$')
        return bool(pattern.match(message.text))
