from typing import Optional

from pydantic import BaseModel

from app.schemas.abstract import TimeAndCashModel


class CharityProjectCreate(BaseModel):
    """Модель Pydantic для создания целевых проектов."""

    name: str
    description: str
    full_amount: int


class CharityProjectDB(CharityProjectCreate, TimeAndCashModel):
    """Модель Pydantic для получения целевых проектов."""

    pass


class CharityProjectUpdate(BaseModel):
    """Модель Pydantic для изменения целевых проектов."""

    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]
