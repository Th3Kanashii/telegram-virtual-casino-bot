from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F
from aiogram.enums import ChatType
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from bot.enums import Locale
from bot.handlers import common
from bot.middlewares.inner import ThrottlingMiddleware
from bot.middlewares.outer import DBSessionMiddleware, UserManager, UserMiddleware
from bot.services.database import create_pool


if TYPE_CHECKING:
    from aiogram import Dispatcher

    from bot.config import Config


def setup_filters(dispatcher: Dispatcher) -> None:
    """
    Sets up filters for the dispatcher.

    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    """
    dispatcher.update.filter(F.chat.type == ChatType.PRIVATE)


def setup_outer_middlewares(dispatcher: Dispatcher, config: Config) -> None:
    """
    Sets up outer middlewares for the dispatcher.

    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    :param config: A configuration object containing necessary settings.
    """
    pool = dispatcher["session_pool"] = create_pool(dsn=config.build_postgres_dsn)
    i18n_middleware = dispatcher["i18n_middleware"] = I18nMiddleware(
        core=FluentRuntimeCore(
            path="locales/{locale}",
            raise_key_error=False,
            locales_map={Locale.JA: Locale.UK, Locale.UK: Locale.EN},
        ),
        manager=UserManager(),
        default_locale=Locale.DEFAULT,
    )

    dispatcher.update.outer_middleware(DBSessionMiddleware(session_pool=pool))
    dispatcher.update.outer_middleware(UserMiddleware())
    i18n_middleware.setup(dispatcher=dispatcher)


def setup_inner_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())
    dispatcher.message.middleware(ThrottlingMiddleware())


def setup_routers(dispatcher: Dispatcher) -> None:
    """
    Sets up routers for the dispatcher.

    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    """
    dispatcher.include_routers(common.router)
