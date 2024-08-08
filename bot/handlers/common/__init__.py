from typing import Final

from aiogram import Router

from . import game, help, language, menu, start


router: Final[Router] = Router(name=__name__)
router.include_routers(start.router, help.router, menu.router, game.router, language.router)
