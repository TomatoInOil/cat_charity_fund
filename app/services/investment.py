from datetime import datetime
from typing import List, Tuple, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_open_donations_in_project(
    project: CharityProject, session: AsyncSession
) -> CharityProject:
    """
    Инвестирует открытые пожертвования в переданный проект.
    Возвращает обновлённый объект переданного проекта.
    """
    donations = await _get_investable_objects_from_db(
        model=Donation, session=session
    )
    remaining_amount = _get_remaining_amount(db_obj=project)
    for oldest_open_donation in donations:
        unallocated_amount = _get_remaining_amount(db_obj=oldest_open_donation)
        (
            remaining_amount,
            unallocated_amount,
            project,
            oldest_open_donation,
        ) = _allocate_amounts(
            remaining_amount, unallocated_amount, project, oldest_open_donation
        )
        oldest_open_donation = check_and_close_fully_invested_object(
            db_obj=oldest_open_donation
        )
        session.add(oldest_open_donation)
        project = check_and_close_fully_invested_object(db_obj=project)
        if remaining_amount == 0:
            break
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


async def invest_donation_in_open_projects(
    donation: Donation, session: AsyncSession
) -> Donation:
    """
    Инвестирует средства переданного пожертвования в открытые проекты.
    Возвращает объект переданного пожертвования.
    """
    projects = await _get_investable_objects_from_db(
        model=CharityProject, session=session
    )
    unallocated_amount = _get_remaining_amount(db_obj=donation)
    for oldest_open_project in projects:
        remaining_amount = _get_remaining_amount(db_obj=oldest_open_project)
        (
            remaining_amount,
            unallocated_amount,
            oldest_open_project,
            donation,
        ) = _allocate_amounts(
            remaining_amount, unallocated_amount, oldest_open_project, donation
        )
        oldest_open_project = check_and_close_fully_invested_object(
            db_obj=oldest_open_project
        )
        session.add(oldest_open_project)
        if unallocated_amount == 0:
            break
    donation = check_and_close_fully_invested_object(db_obj=donation)
    session.add(donation)
    await session.commit()
    await session.refresh(donation)
    return donation


def check_and_close_fully_invested_object(
    db_obj: Union[Donation, CharityProject]
) -> Union[Donation, CharityProject]:
    """
    Проверяет, что объект полностью инвестирован.
    Если утверждение верно, то закрывает его.
    """
    if db_obj.invested_amount == db_obj.full_amount:
        db_obj.fully_invested = True
        db_obj.close_date = datetime.now()
    return db_obj


async def _get_investable_objects_from_db(
    model: Union[Donation, CharityProject], session: AsyncSession
) -> List[Union[Donation, CharityProject]]:
    """Получение открытых к инвестированию объектов из БД."""
    db_objs = await session.execute(
        select(model)
        .where(model.fully_invested.is_(False))
        .order_by(model.create_date.asc())
    )
    db_objs = db_objs.scalars().all()
    return db_objs


def _allocate_amounts(
    remaining_amount: int,
    unallocated_amount: int,
    project: CharityProject,
    donation: Donation,
) -> Tuple[int, int, CharityProject, Donation]:
    """Переводит средства из пожертвования в проект."""
    if remaining_amount >= unallocated_amount:
        project.invested_amount += unallocated_amount
        donation.invested_amount += unallocated_amount
        remaining_amount -= unallocated_amount
        unallocated_amount = 0
    else:
        project.invested_amount += remaining_amount
        donation.invested_amount += remaining_amount
        unallocated_amount -= remaining_amount
        remaining_amount = 0
    return remaining_amount, unallocated_amount, project, donation


def _get_remaining_amount(db_obj: Union[Donation, CharityProject]) -> int:
    """Возвращает разницу между полными и инвестированными средствами"""
    result = db_obj.full_amount - db_obj.invested_amount
    return result
