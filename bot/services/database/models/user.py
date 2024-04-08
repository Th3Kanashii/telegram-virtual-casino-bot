from __future__ import annotations

from aiogram import html
from aiogram.types import User
from aiogram.utils.link import create_tg_link
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64, TimestampMixin


class DBUser(Base, TimestampMixin):
    """
    Model for the users table.
    """

    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    locale: Mapped[str] = mapped_column(String(length=2), nullable=False)
    balance: Mapped[int] = mapped_column(nullable=False, default=0)
    refferal: Mapped[Int64] = mapped_column(nullable=True)

    @property
    def url(self) -> str:
        """
        :return: URL of the user.
        """
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        """
        :return: Mention of the user.
        """
        return html.link(value=self.name, link=self.url)

    @classmethod
    def from_aiogram(cls, user: User, locale: str) -> DBUser:
        """
        Create an instance of the model from an aiogram User object.

        :param user: User object from aiogram.
        :param locale: User's locale.
        :return: Instance of the model.
        """
        return DBUser(id=user.id, name=user.full_name, locale=locale)
