"""SQLAlchemy mapping for the existing usage_records table."""

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UsageRecord(Base):
    __tablename__ = "usage_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(100))
    team: Mapped[str] = mapped_column(String(100))
    tool: Mapped[str] = mapped_column(String(50))
    tokens: Mapped[int] = mapped_column(Integer)
    cost: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    used_on: Mapped[date] = mapped_column(Date)
