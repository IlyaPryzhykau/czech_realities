from pydantic_settings import BaseSettings
from pydantic import EmailStr
from pathlib import Path


class Settings(BaseSettings):
    app_title: str
    description: str
    database_url: str
    secret: str
    first_superuser_email: EmailStr | None = None
    first_superuser_password: str | None = None

    class Config:
        env_file = str(Path(__file__).resolve().parents[2] / '.env')
        env_file_encoding = "utf-8"


settings = Settings()
