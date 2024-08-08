from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .user import UserRepository


class Repository(BaseRepository):
    """
    The general repository.
    """

    user: UserRepository

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the repository.

        :param session: The database session.
        """
        super().__init__(session=session)
        self.user = UserRepository(session=session)
