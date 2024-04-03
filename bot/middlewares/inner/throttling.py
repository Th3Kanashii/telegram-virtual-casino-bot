from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware for throttling message processing based on specified limits.
    """

    def __init__(self) -> None:
        """
        Initializes ThrottlingMiddleware with a specified throttling limit.
        """
        self.cache: Dict[str, TTLCache] = {
            "default": TTLCache(maxsize=100, ttl=1),
        }

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Optional[Any]:
        throttling_key = get_flag(data, "throttling_key")

        if throttling_key is not None and throttling_key in self.cache:
            if event.chat.id in self.cache[throttling_key]:
                return None
            self.cache[throttling_key][event.chat.id] = None
        return await handler(event, data)
