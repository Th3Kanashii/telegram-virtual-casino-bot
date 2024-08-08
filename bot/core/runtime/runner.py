from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher

from .polling import polling_shutdown, polling_startup


def run_polling(bot: Bot, dispatcher: Dispatcher) -> None:
    """
    Run the bot in the polling mode.

    :param bot: An instance of the Telegram bot.
    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    """
    dispatcher.startup.register(polling_startup)
    dispatcher.shutdown.register(polling_shutdown)
    dispatcher.run_polling(bot)
