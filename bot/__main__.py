from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher

from .config import Config
from .core.factory import create_bot, create_dispatcher
from .core.runtime import run_polling
from .utils.logging import setup_logger


def main() -> None:
    setup_logger()
    config: Config = Config()
    dispatcher: Dispatcher = create_dispatcher(config=config)
    bot: Bot = create_bot(config=config)
    run_polling(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    asyncio.run(main())
