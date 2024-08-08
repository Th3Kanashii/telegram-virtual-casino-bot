from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


if TYPE_CHECKING:
    from bot.config import Config


def create_bot(config: Config) -> Bot:
    """
    Creates a Telegram bot instance.

    :param config: A configuration object containing necessary settings.
    :return: An instance of the Telegram bot.
    """
    return Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
