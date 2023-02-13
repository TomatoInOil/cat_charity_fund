from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_invested_amount_before_delete,
    check_project_data_before_update,
    check_project_name_exists,
)
from app.services.investment import invest_open_donations_in_project
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
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
    return await charity_project_crud.get_all(session=session)


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
    await check_project_name_exists(name=obj_in.name, session=session)
    project = await charity_project_crud.create(obj_in=obj_in, session=session)
    project = await invest_open_donations_in_project(
        project=project, session=session
    )
    return project


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
    project = await charity_project_crud.get_or_404(
        obj_id=project_id, session=session
    )
    check_invested_amount_before_delete(project)
    await charity_project_crud.delete(db_obj=project, session=session)
    return project


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
    project = await charity_project_crud.get_or_404(
        obj_id=project_id, session=session
    )
    await check_project_data_before_update(
        db_obj=project, obj_in=obj_in, session=session
    )
    if project.invested_amount == obj_in.full_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
    project = await charity_project_crud.update(
        db_obj=project, obj_in=obj_in, session=session
    )
    return project
