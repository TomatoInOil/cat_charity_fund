from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_invested_amount_before_delete,
    check_project_data_before_update,
    check_project_name_exists,
    get_charity_project_or_404,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    all_projects = await session.execute(select(CharityProject))
    return all_projects.scalars().all()


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_charity_project(
    obj_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создаёт благотворительный проект.
    Только для суперюзеров.
    """
    obj_in_data = obj_in.dict()
    await check_project_name_exists(name=obj_in_data["name"], session=session)
    db_obj = CharityProject(**obj_in_data)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    """
    Удаляет проект. Нельзя удалить проект, в который уже были
    инвестированы средства, его можно только закрыть.
    Только для суперюзеров.
    """
    db_obj = await get_charity_project_or_404(
        project_id=project_id, session=session
    )
    check_invested_amount_before_delete(db_obj)
    await session.delete(db_obj)
    await session.commit()
    return db_obj


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Закрытый проект нельзя редактировать; нельзя установить
    требуемую сумму меньше уже вложенной.
    Только для суперюзеров.
    """
    db_obj = await get_charity_project_or_404(
        project_id=project_id, session=session
    )
    db_obj_data = jsonable_encoder(db_obj)
    obj_in_data = obj_in.dict(exclude_unset=True)
    await check_project_data_before_update(db_obj_data, obj_in_data, session)
    for field in db_obj_data:
        if field in obj_in_data:
            setattr(db_obj, field, obj_in_data[field])
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj
