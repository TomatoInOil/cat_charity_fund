from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Модель Pydantic для получения информации о пользователях."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Модель Pydantic для регистрации пользователя."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Модель Pydantic для изменение профиля пользователя."""

    pass
