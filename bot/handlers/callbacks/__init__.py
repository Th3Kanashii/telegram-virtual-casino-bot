from typing import Final

from aiogram import Router

from . import factories, game, menu

router: Final[Router] = Router(name=__name__)
router.include_routers(factories.router, game.router, menu.router)
