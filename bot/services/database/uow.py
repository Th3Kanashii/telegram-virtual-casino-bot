from sqlalchemy.ext.asyncio import AsyncSession

from .models import Base


class UoW:
    """
    Unit of Work.
    """

    _session: AsyncSession

    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the unit of work.

        :param session: The database session.
        """
        self._session = session

    async def commit(self, *instances: Base) -> None:
        """
        Commit the given instances to the database.
        """
        self._session.add_all(instances)
        await self._session.commit()
