from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from ..enums import Back, Game, Locale, Menu, Operation
from .factories import Bet, Games, Language


def select_language(i18n: I18nContext) -> InlineKeyboardMarkup:
    """
    Select language keyboard

    :param i18n: I18nContext
    :return: InlineKeyboardMarkup with language selection
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard.row(
        *[
            InlineKeyboardButton(text="🇬🇧", callback_data=Language(language=Locale.EN).pack()),
            InlineKeyboardButton(text="🇺🇦", callback_data=Language(language=Locale.UK).pack()),
            InlineKeyboardButton(text="🇯🇵", callback_data=Language(language=Locale.JA).pack()),
            InlineKeyboardButton(text=i18n.get("button-back"), callback_data=Back.DEFAULT),
        ],
        width=1,
    )
    return keyboard.as_markup()


def menu(i18n: I18nContext) -> InlineKeyboardMarkup:
    """
    Create an inline keyboard for the menu.

    :param i18n: The i18n context.
    :return: The inline keyboard.
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=i18n.get("button-games"), callback_data=Menu.GAMES))
    keyboard.row(
        InlineKeyboardButton(text=i18n.get("button-language"), callback_data=Menu.LANGUAGE),
        InlineKeyboardButton(text=i18n.get("button-support"), url="https://t.me/Th3Kanashii"),
        width=2,
    )
    return keyboard.as_markup()


def games(i18n: I18nContext) -> InlineKeyboardMarkup:
    """
    Create an inline keyboard for the games.

    :param i18n: The i18n context.
    :return: The inline keyboard.
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard.row(
        *[
            InlineKeyboardButton(
                text=i18n.get("button-slots"), callback_data=Games(game=Game.SLOTS).pack()
            ),
            InlineKeyboardButton(
                text=i18n.get("button-dice"), callback_data=Games(game=Game.DICE).pack()
            ),
            InlineKeyboardButton(
                text=i18n.get("button-basket"), callback_data=Games(game=Game.BASKET).pack()
            ),
            InlineKeyboardButton(
                text=i18n.get("button-darts"), callback_data=Games(game=Game.DARTS).pack()
            ),
            InlineKeyboardButton(
                text=i18n.get("button-bowling"), callback_data=Games(game=Game.BOWLING).pack()
            ),
            InlineKeyboardButton(
                text=i18n.get("button-football"), callback_data=Games(game=Game.FOOTBALL).pack()
            ),
            InlineKeyboardButton(text=i18n.get("button-back"), callback_data=Back.DEFAULT),
        ],
        width=2,
    )
    return keyboard.as_markup()


def play(i18n: I18nContext, game: str, bet: int = 10) -> InlineKeyboardMarkup:
    """
    Create an inline keyboard for the play.

    :param i18n: The i18n context.
    :return: The inline keyboard.
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard.row(
        *[
            InlineKeyboardButton(text="-", callback_data=Bet(operation=Operation.SUB).pack()),
            InlineKeyboardButton(text=f"{bet} 💎", callback_data=Operation.DEFAULT),
            InlineKeyboardButton(text="+", callback_data=Bet(operation=Operation.ADD).pack()),
            InlineKeyboardButton(
                text=i18n.get("button-min"), callback_data=Bet(operation=Operation.MIN).pack()
            ),
            InlineKeyboardButton(
                text=i18n.get("button-double"),
                callback_data=Bet(operation=Operation.DOUBLE).pack(),
            ),
            InlineKeyboardButton(
                text=i18n.get("button-max"), callback_data=Bet(operation=Operation.MAX).pack()
            ),
            InlineKeyboardButton(text=i18n.get("button-back"), callback_data=Back.GAME),
            InlineKeyboardButton(text=i18n.get(f"{game}-play"), callback_data=f"{game}-play"),
        ],
        width=3,
    )
    return keyboard.as_markup()
