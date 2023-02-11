from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.schemas.abstract import TimeAndCashModel


class CharityProjectCreate(BaseModel):
    """Модель Pydantic для создания целевых проектов."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(BaseModel):
    """Модель Pydantic для изменения целевых проектов."""

    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate, TimeAndCashModel):
    """Модель Pydantic для получения целевых проектов."""

    id: int

    class Config:
        orm_mode = True
