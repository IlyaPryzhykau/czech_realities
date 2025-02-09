"""
This module defines application-wide settings using Pydantic's BaseSettings.
It automatically loads environment variables from a .env file.
"""

from pydantic_settings import BaseSettings
from pydantic import EmailStr
from pathlib import Path


class Settings(BaseSettings):
    """
    Application settings managed by Pydantic.

    Attributes:
        app_title (str): The title of the application.
        description (str): A short description for the application.
        database_url (str): The database URL for SQLAlchemy connections.
        secret (str): A secret key used for cryptographic operations.
        first_superuser_email (EmailStr | None): An optional superuser email.
        first_superuser_password (str | None): An optional superuser password.
    """
    app_title: str
    description: str
    database_url: str
    secret: str
    first_superuser_email: EmailStr | None = None
    first_superuser_password: str | None = None

    class Config:
        """
        Configuration class for Settings.

        Specifies the .env file location and encoding.
        """
        env_file = str(Path(__file__).resolve().parents[2] / '.env')
        extra = 'ignore'
        env_file_encoding = 'utf-8'


settings = Settings()
