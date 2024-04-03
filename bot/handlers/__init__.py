from aiogram import Dispatcher, F

from .common import common_router
from .game import game_router
from .menu import menu_router


def _setup_routers(dispatcher: Dispatcher) -> None:
    """
    Include routers in the dispatcher.

    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    """
    dispatcher.message.filter(F.chat.type == "private")
    dispatcher.include_routers(
        common_router,
        menu_router,
        game_router,
    )


__all__ = [
    "_setup_routers",
]
