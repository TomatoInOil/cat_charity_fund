from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
    if obj_in_data["full_amount"] <= 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Требуемая сумма должна быть целочисленной и больше 0",
        )
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
    db_obj = await session.execute(
        select(CharityProject).where(CharityProject.id == project_id)
    )
    db_obj = db_obj.scalars().first()
    if db_obj.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Нельзя удалить проект, в который "
                "уже были инвестированы средства."
            ),
        )
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
    db_obj = await session.execute(
        select(CharityProject).where(CharityProject.id == project_id)
    )
    db_obj = db_obj.scalars().first()
    if db_obj is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Благотворительный проект с {project_id} не найден",
        )
    if db_obj.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )
    db_obj_data = jsonable_encoder(db_obj)
    obj_in_data = obj_in.dict(exclude_unset=True)
    new_name = obj_in_data.get("name")
    if new_name is not None:
        await check_project_name_exists(name=new_name, session=session)
    full_amount = obj_in_data.get("full_amount")
    if full_amount is not None:
        if obj_in_data.get("full_amount") < db_obj.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Нельзя установить требуемую сумму меньше уже вложенной",
            )
    for field in db_obj_data:
        if field in obj_in_data:
            setattr(db_obj, field, obj_in_data[field])
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def check_project_name_exists(name: str, session: AsyncSession):
    """Вызывает исключение, если проект с таким именем уже существует."""
    project_found_by_name = await session.execute(
        select(CharityProject).where(CharityProject.name == name)
    )
    project_found_by_name = project_found_by_name.first()
    if project_found_by_name is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )
