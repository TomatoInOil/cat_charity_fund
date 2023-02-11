from typing import Optional

from pydantic import BaseModel

from app.schemas.abstract import TimeAndCashModel


class DonationCreate(BaseModel):
    """Модель Pydantic для создания пожертвования."""

    comment: Optional[str]
    full_amount: int


class DonationtDB(DonationCreate, TimeAndCashModel):
    """Модель Pydantic для получения информации о пожертвовании."""

    class Config:
        orm_mode = True
