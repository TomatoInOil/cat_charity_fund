from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.abstract import TimeAndCashModel


class DonationCreate(BaseModel):
    """Модель Pydantic для создания пожертвования."""

    comment: Optional[str]
    full_amount: int


class DonationtDB(DonationCreate):
    """Модель Pydantic для получения информации о пожертвовании."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class ExtendedDonationtDB(DonationtDB, TimeAndCashModel):
    """Модель Pydantic для получшения всей информации о пожертвовании."""

    user_id: int
