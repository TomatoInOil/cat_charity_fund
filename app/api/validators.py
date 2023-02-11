from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject


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
            detail=(
                "Нельзя удалить проект, в который "
                "уже были инвестированы средства."
            ),
        )


async def get_charity_project_or_404(project_id: int, session: AsyncSession):
    """Возвращает объект целевого проекта из БД или вызывает ошибку 404."""
    db_obj = await session.execute(
        select(CharityProject).where(CharityProject.id == project_id)
    )
    db_obj = db_obj.scalars().first()
    if db_obj is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Благотворительный проект с {project_id} не найден",
        )
    return db_obj


async def check_project_data_before_update(
    db_obj_data: dict, obj_in_data: dict, session: AsyncSession
):
    """
    Валидация перед изменением проекта.
    Вызывает исключение, если проект закрыт, если имя неуникально,
    если требуемая сумма меньше вложенной.
    """
    if db_obj_data["fully_invested"] is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )

    new_name = obj_in_data.get("name")
    if new_name is not None:
        await check_project_name_exists(name=new_name, session=session)

    full_amount = obj_in_data.get("full_amount")
    if full_amount is not None:
        if obj_in_data.get("full_amount") < db_obj_data["invested_amount"]:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Нельзя установить требуемую сумму меньше уже вложенной",
            )
