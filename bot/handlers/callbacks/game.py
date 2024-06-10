from __future__ import annotations

import asyncio
import secrets
from typing import TYPE_CHECKING, Dict, Final

from aiogram import F, Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from ...enums import Game
from ...keyboards import play
from ...misc import calculate_game_result

if TYPE_CHECKING:
    from ...services.database import DBUser, UoW

dices: Final[Dict[Game, DiceEmoji]] = {
    Game.DICE: DiceEmoji.DICE,
    Game.FOOTBALL: DiceEmoji.FOOTBALL,
    Game.BASKET: DiceEmoji.BASKETBALL,
    Game.DARTS: DiceEmoji.DART,
    Game.BOWLING: DiceEmoji.BOWLING,
    Game.SLOTS: DiceEmoji.SLOT_MACHINE,
}
router: Final[Router] = Router(name=__name__)


@router.callback_query(F.data == Game.PLAY)
async def play_game(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext, user: DBUser, uow: UoW
) -> None:
    """
    Play the game.

    :param callback: The callback query.
    :param state: The FSM state.
    :param i18n: The i18n context.
    :param user: The user.
    :param uow: The unit of work.
    """
    data = await state.get_data()
    if user.balance < data["bet"]:
        await callback.message.edit_text(text=i18n.get("zero-balance"))
        return

    game: Message = await callback.message.edit_text(i18n.get("good-luck"))
    dice: Message = await callback.message.answer_dice(emoji=dices[data["game"]])

    result = calculate_game_result(
        game=data["game"], bet_amount=data["bet"], dice_value=dice.dice.value
    )
    lose = secrets.choice(i18n.get("lose").split(","))
    await asyncio.sleep(2)

    user.balance += round(result)
    await uow.commit(user)
    await game.edit_text(text=i18n.get("win", number=result - data["bet"]) if result > 0 else lose)
    await callback.message.answer(
        text=i18n.get(data["game"], balance=user.balance),
        reply_markup=play(i18n=i18n, game=data["game"], bet=data["bet"]),
    )
