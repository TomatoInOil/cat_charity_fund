from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationtDB

router = APIRouter()


@router.get(
    "/",
    response_model=List[DonationtDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возвращает список всех пожертвований.
    Только для суперюзеров.
    """
    return await donation_crud.get_all(session=session)


@router.post("/", response_model=DonationtDB)
async def create_donation(
    obj_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    donation = await donation_crud.create(
        obj_in=obj_in, session=session, user_id=user.id
    )
    # процесс инвестирования
    return donation


@router.get("/my", response_model=DonationtDB)
async def get_user_donations():
    """Получить список пожертвований пользователя, выполняющего запрос."""
    pass
