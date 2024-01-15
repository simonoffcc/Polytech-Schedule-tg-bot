"""from aiogram.types import Message
from aiogram.filters import BaseFilter

from src.bot.middlewares import DatabaseMiddleware
from src.db import Database


class RegisterFilter(BaseFilter):
    async def __call__(self, data: Database) -> bool:
        result = await UserRepo.user_exists(user_id=message.from_user.id)
        return result
"""