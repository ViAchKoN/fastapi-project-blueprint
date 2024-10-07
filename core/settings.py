import typing

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_USER: typing.Optional[str] = Field(
        env="DATABASE_USERNAME",
        default='postgres',
    )
    DATABASE_PASSWORD: typing.Optional[str] = Field(
        env='DATABASE_PASSWORD',
        default='postgres',
    )
    DATABASE_HOST: typing.Optional[str] = Field(
        env='DATABASE_HOST',
        default='localhost',
    )
    DATABASE_PORT: typing.Optional[int] = Field(
        env='DATABASE_PORT',
        default=5432,
    )
    DATABASE_NAME: typing.Optional[str] = Field(
        env='DATABASE_NAME',
        default='fastapi_project_base',
    )


settings = Settings()

DB_URL: typing.Optional[str] = f'postgresql+psycopg2://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
