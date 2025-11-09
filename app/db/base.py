from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models for Alembic's autogeneration discovery.
from app.models.user import User  # noqa: E402,F401


__all__ = ("Base", "User")

