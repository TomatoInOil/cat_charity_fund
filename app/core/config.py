from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки проекта QRKot."""

    app_title: str = "Благотворительный фонд поддержки котиков QRKot"
    description: str = (
        "Фонд собирает пожертвования на различные целевые "
        "проекты, направленные на помощь хвостатым."
    )
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"

    class Config:
        env_file = ".env"


settings = Settings()
