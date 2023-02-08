from core.db import Base
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.sql import func


class CharityProject(Base):
    """Модель SQLAlchemy для целевого проекта."""

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(
        Integer,
        CheckConstraint("full_amount > 0", name="check_full_amount_positive"),
    )
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=func.now())
    close_date = Column(DateTime)
