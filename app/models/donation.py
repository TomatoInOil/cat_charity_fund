from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.abstract import CashColumnsModel, TimeColumnsModel


class Donation(TimeColumnsModel, CashColumnsModel):
    """Модель SQLAlchemy для пожертвований."""

    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))
