"""User model file."""
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    """User model."""

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False
    )
    user_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    institute_id: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=True
    )
    group_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=False, nullable=True
    )
    institute_abbr: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    group_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
