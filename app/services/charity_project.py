from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_open_donations_in_project(
    project: CharityProject, session: AsyncSession
):
    """
    Инвестирует открытые пожертвования в переданный проект.
    Возвращает обновлённый объект переданного проекта.
    """
    donations = await session.execute(
        select(Donation)
        .where(Donation.fully_invested.is_(False))
        .order_by(Donation.create_date.asc())
    )
    donations = donations.scalars().all()
    remaining_amount = project.full_amount
    for donation in donations:
        unallocated_amount = donation.full_amount - donation.invested_amount
        if remaining_amount >= unallocated_amount:
            project.invested_amount += unallocated_amount
            remaining_amount -= unallocated_amount
        else:
            project.invested_amount += remaining_amount
        unallocated_amount -= remaining_amount

        donation.invested_amount = donation.full_amount - unallocated_amount
        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.now()
        session.add(donation)

        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
            break
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project
