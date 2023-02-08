from typing import List

from fastapi import APIRouter

from app.schemas.donations import DonationCreate, DonationtDB

router = APIRouter()


@router.get("/", response_model=List[DonationtDB])
async def get_all_donations():
    """
    Возвращает список всех пожертвований.
    Только для суперюзеров.
    """
    pass


@router.post("/", response_model=DonationtDB)
async def create_donation(obj_in: DonationCreate):
    """Сделать пожертвование."""
    pass


@router.get("/my", response_model=DonationtDB)
async def get_user_donations():
    """Получить список пожертвований пользователя, выполняющего запрос."""
    pass
