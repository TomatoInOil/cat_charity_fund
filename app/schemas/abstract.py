from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TimeAndCashModel(BaseModel):
    """
    Абстрактная модель Pydantic для пожертвований и проектов.
    Содержит поля времени и поля для подсчёта денежных средств.
    """

    invested_amount: int = Field(ge=0)
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
