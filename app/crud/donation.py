from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models import Donation


class DonationCRUD(BaseCRUD):
    """Расширение CRUD для модели пожертвований."""

    async def get_by_user(self, user_id: int, session: AsyncSession):
        """Получение объектов из БД, созданных пользователем."""
        db_objs = await session.execute(
            select(self.model).where(user_id=user_id)
        )
        return db_objs.scalars().all()


donation_crud = DonationCRUD(model=Donation)
