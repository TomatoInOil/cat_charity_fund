from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate
from app.schemas.donation import DonationCreate


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


def check_invested_amount_before_delete(db_obj: CharityProject):
    """Вызывает исключение, если в проект уже были инвестированы средства."""
    if db_obj.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


async def check_project_data_before_update(
    db_obj: CharityProject, obj_in: CharityProjectUpdate, session: AsyncSession
):
    """
    Валидация перед изменением проекта.
    Вызывает исключение, если проект закрыт, если имя неуникально,
    если требуемая сумма меньше вложенной.
    """
    if db_obj.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )

    new_name = obj_in.name
    if new_name is not None:
        await check_project_name_exists(name=new_name, session=session)

    new_full_amount = obj_in.full_amount
    if new_full_amount is not None:
        if new_full_amount < db_obj.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Нельзя установить требуемую сумму меньше уже вложенной",
            )


def check_donation_amount_is_positive(obj_in: DonationCreate):
    """Вызывает исключение, если сумма пожертвований неположительна."""
    if obj_in.full_amount <= 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Сумма пожертвования должна быть целой и положительной!",
        )
