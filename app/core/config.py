from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки проекта QRKot."""

    app_title: str = "Благотворительный фонд поддержки котиков QRKot"
    app_description: str = (
        "Фонд собирает пожертвования на различные целевые "
        "проекты, направленные на помощь хвостатым."
    )
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    admin_email: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
