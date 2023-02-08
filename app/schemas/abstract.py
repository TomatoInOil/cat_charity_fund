from datetime import datetime

from pydantic import BaseModel


class TimeAndCashModel(BaseModel):
    """
    Абстрактная модель Pydantic для пожертвований и проектов.
    Содержит поля времени и поля для подсчёта денежных средств.
    """

    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_Date: datetime
