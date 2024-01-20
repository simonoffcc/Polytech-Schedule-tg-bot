from aiogram.types import Message
from aiogram.filters import BaseFilter

from src.db import Database


class RegisterFilter(BaseFilter):
    async def __call__(self, message: Message, **kwargs) -> bool:
        db: Database = kwargs.get('db')
        result = await db.user.is_user_exists(user_id=message.from_user.id)
        return result
