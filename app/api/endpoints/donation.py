from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate,
    DonationtDB,
    ExtendedDonationtDB,
)
from app.services.donation import invest_donation_in_open_projects
from app.api.validators import check_donation_amount_is_positive

router = APIRouter()


@router.get(
    "/",
    response_model=List[ExtendedDonationtDB],
    response_model_exclude_none=True,
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


@router.post(
    "/",
    response_model=DonationtDB,
    response_model_exclude_none=True,
)
async def create_donation(
    obj_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    check_donation_amount_is_positive(obj_in=obj_in)
    donation = await donation_crud.create(
        obj_in=obj_in, session=session, user_id=user.id
    )
    donation = await invest_donation_in_open_projects(donation=donation, session=session)
    return donation


@router.get("/my", response_model=List[DonationtDB])
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получить список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_by_user(user_id=user.id, session=session)
