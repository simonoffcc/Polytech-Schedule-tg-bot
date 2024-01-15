from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message

from src.bot.structures.data_structure import TransferData
from src.db.database import Database


class RegisterMiddleware(BaseMiddleware):
    """
    This class is used for checking if user already exists in database.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        db: Database = data['db']
        result = await db.user.user_exists(user_id=event.from_user.id)
        data['is_register'] = result
        return await handler(event, data)
