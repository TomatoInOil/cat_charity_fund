from sqlalchemy import Column, String, Text

from app.models.abstract import CashColumnsModel, TimeColumnsModel


class CharityProject(TimeColumnsModel, CashColumnsModel):
    """Модель SQLAlchemy для целевого проекта."""

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
