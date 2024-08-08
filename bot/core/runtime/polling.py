from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def polling_startup(bot: Bot) -> None:
    """
    Starts the bot in the polling mode.

    :param bot: An instance of the Telegram bot.
    """
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="🔄 Restart the bot"),
            BotCommand(command="help", description="🤝 Get help"),
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )
    await bot.delete_webhook(drop_pending_updates=True)


async def polling_shutdown(bot: Bot, dispatcher: Dispatcher) -> None:
    """
    Stops the bot in the polling mode.

    :param bot: An instance of the Telegram bot.
    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    """
    session_pool: async_sessionmaker[AsyncSession] = dispatcher["session_pool"]
    async with session_pool() as session:
        await session.close_all()
        await session.bind.dispose()

    await dispatcher.storage.close()
    await bot.session.close()
