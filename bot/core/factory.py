from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from redis.asyncio import ConnectionPool, Redis

from ..enums import Locale
from ..handlers import _setup_routers
from ..middlewares import DBSessionMiddleware, ThrottlingMiddleware, UserManager, UserMiddleware
from ..services.database import create_pool

if TYPE_CHECKING:
    from ..config import Config


def _setup_outer_middlewares(dispatcher: Dispatcher, config: Config) -> None:
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


def _setup_inner_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())
    dispatcher.message.middleware(ThrottlingMiddleware())


def create_dispatcher(config: Config) -> Dispatcher:
    """
    Creates and configures a Telegram bot dispatcher.

    :param config: A configuration object containing necessary settings.
    :return: An instance of the Dispatcher for the Telegram bot.
    """
    redis: Redis = Redis(
        connection_pool=ConnectionPool(
            host=config.redis_host,
            port=config.redis_port,
            db=config.redis_db,
        )
    )
    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher", storage=RedisStorage(redis=redis), config=config
    )
    _setup_routers(dispatcher=dispatcher)
    _setup_outer_middlewares(dispatcher=dispatcher, config=config)
    _setup_inner_middlewares(dispatcher=dispatcher)
    return dispatcher


def create_bot(config: Config) -> Bot:
    """
    Creates a Telegram bot instance.

    :param config: A configuration object containing necessary settings.
    :return: An instance of the Telegram bot.
    """
    session: AiohttpSession = AiohttpSession()
    return Bot(
        token=config.bot_token.get_secret_value(),
        parse_mode=ParseMode.HTML,
        session=session,
    )
