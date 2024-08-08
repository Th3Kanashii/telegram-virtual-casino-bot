from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """
    Base class for all repositories.
    """

    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the repository.

        :param session: The database session.
        """
        self._session = session
