from sqlalchemy import Column, Text

from app.models.abstract import CashColumnsModel, TimeColumnsModel


class Donation(TimeColumnsModel, CashColumnsModel):
    """Модель SQLAlchemy для пожертвований."""

    comment = Column(Text, nullable=True)
