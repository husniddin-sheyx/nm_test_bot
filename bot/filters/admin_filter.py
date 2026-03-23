from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from bot.config import ADMIN_IDS

class AdminFilter(BaseFilter):
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        return event.from_user.id in ADMIN_IDS
