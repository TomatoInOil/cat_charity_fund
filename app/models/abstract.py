from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer
from sqlalchemy.sql import func

from app.core.db import Base


class TimeColumnsModel(Base):
    """Абстрактная модель SQLAlchemy с полями времени."""

    __abstract__ = True
    create_date = Column(DateTime, default=func.now())
    close_date = Column(DateTime)


class CashColumnsModel(Base):
    """Абстрактная модель SQLAlchemy с полями для подсчёта денежных средств."""

    __abstract__ = True
    full_amount = Column(
        Integer,
        CheckConstraint("full_amount > 0", name="check_full_amount_positive"),
    )
    fully_invested = Column(Boolean, default=False)
    invested_amount = Column(Integer, default=0)
