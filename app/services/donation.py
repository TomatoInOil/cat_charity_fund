from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_donation_in_open_projects(
    donation: Donation, session: AsyncSession
):
    """
    Инвестирует средства переданного пожертвования в открытые проекты.
    Возвращает объект переданного пожертвования.
    """
    projects = await session.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested.is_(False))
        .order_by(CharityProject.create_date.asc())
    )
    projects = projects.scalars().all()
    unallocated_amount = donation.full_amount - donation.invested_amount
    for oldest_open_project in projects:
        remaining_amount = (
            oldest_open_project.full_amount
            - oldest_open_project.invested_amount
        )
        if remaining_amount >= unallocated_amount:
            oldest_open_project.invested_amount += unallocated_amount
            unallocated_amount = 0
        else:
            oldest_open_project.invested_amount += remaining_amount
            unallocated_amount -= remaining_amount

        if (
            oldest_open_project.invested_amount
            == oldest_open_project.full_amount
        ):
            oldest_open_project.fully_invested = True
            oldest_open_project.close_date = datetime.now()
        session.add(oldest_open_project)

        if unallocated_amount == 0:
            break
    donation.invested_amount = donation.full_amount - unallocated_amount
    if donation.invested_amount == donation.full_amount:
        donation.fully_invested = True
        donation.close_date = datetime.now()
    session.add(donation)
    await session.commit()
    await session.refresh(donation)
    return donation
