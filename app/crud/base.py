from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD:
    """Абстрактная реализация CRUD."""

    NOT_FOUND_MSG = "Объект с переданным id не найден."

    def __init__(self, model) -> None:
        self.model = model

    async def get_all(self, session: AsyncSession):
        """Получить все объекты из БД."""
        all_db_objs = await session.execute(select(self.model))
        return all_db_objs.scalars().all()

    async def create(
        self, obj_in, session: AsyncSession, user_id: Optional[int] = None
    ):
        """Создание объекта и сохранение в БД. Возвращает объект."""
        obj_in_data = obj_in.dict()
        if user_id is not None:
            obj_in_data["user_id"] = user_id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_or_404(self, obj_id: int, session: AsyncSession):
        """Получение объекта из БД, иначе вызов ошибки 404."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        db_obj = db_obj.scalars().first()
        if db_obj is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=self.NOT_FOUND_MSG,
            )
        return db_obj

    async def delete(self, db_obj, session: AsyncSession):
        """Удалить объект из БД. Ничего не возвращает."""
        await session.delete(db_obj)
        await session.commit()

    async def update(self, db_obj, obj_in, session: AsyncSession):
        """Обновляет объект в БД. Возвращает обновлённый объект."""
        project_data = jsonable_encoder(db_obj)
        obj_in_data = obj_in.dict(exclude_unset=True)
        for field in project_data:
            if field in obj_in_data:
                setattr(db_obj, field, obj_in_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
