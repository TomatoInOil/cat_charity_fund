from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CharityProjectCreate(BaseModel):
    """Модель Pydantic для создания целевых проектов."""

    name: str
    description: str
    full_amount: int


class CharityProjectDB(CharityProjectCreate):
    """Модель Pydantic для получения целевых проектов."""

    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_Date: datetime


class CharityProjectUpdate(BaseModel):
    """Модель Pydantic для изменения целевых проектов."""

    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]
