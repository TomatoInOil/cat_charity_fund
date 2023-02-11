from sqlalchemy import Column, String, Text

from app.models.abstract import TimeColumnsModel, CashColumnsModel


class CharityProject(TimeColumnsModel, CashColumnsModel):
    """Модель SQLAlchemy для целевого проекта."""

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
