from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from bot.services.database import get_user_language

class I18nMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user: User = data.get("event_from_user")
        if user:
            lang = get_user_language(user.id)
            data["lang"] = lang
        else:
            data["lang"] = "uz"
            
        return await handler(event, data)
