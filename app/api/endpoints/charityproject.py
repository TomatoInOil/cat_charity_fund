from typing import List

from fastapi import APIRouter

from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[CharityProjectDB])
async def get_all_charity_projects():
    """Возвращает список всех проектов."""
    pass


@router.post("/", response_model=CharityProjectDB)
async def create_charity_project(obj_in: CharityProjectCreate):
    """
    Создаёт благотворительный проект.
    Только для суперюзеров.
    """
    pass


@router.delete("/{project_id}", response_model=CharityProjectDB)
async def delete_charity_project(project_id: int):
    """
    Удаляет проект. Нельзя удалить проект, в который уже были
    инвестированы средства, его можно только закрыть.
    Только для суперюзеров.
    """
    pass


@router.patch("/{project_id}", response_model=CharityProjectDB)
async def update_charity_project(
    project_id: int, obj_in: CharityProjectUpdate
):
    """
    Закрытый проект нельзя редактировать; нельзя установить
    требуемую сумму меньше уже вложенной.
    Только для суперюзеров.
    """
    pass
