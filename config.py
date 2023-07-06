import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY')
    JTW_ALGORITHM:  str = 'HS256'
    JWT_EXPIRES_S:  int = 86400

    POSTGRES_USER:     str = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_HOSTNAME: str = os.environ.get('POSTGRES_HOSTNAME')
    POSTGRES_PORT:     str = os.environ.get('POSTGRES_PORT')
    POSTGRES_DB:       str = os.environ.get('POSTGRES_DB')
    POSTGRES_DB_TEST:  str = os.environ.get('POSTGRES_DB_TEST')

    class Config:
        env_file = ".env"


def get_db_url(test: bool = False):
    if not test:
        url = 'postgresql+psycopg2://{user}:{psw}@{url}/{db}'.format(
            user=Settings().POSTGRES_USER,
            psw=Settings().POSTGRES_PASSWORD,
            url=f"{Settings().POSTGRES_HOSTNAME}:"
                f"{Settings().POSTGRES_PORT}",
            db=Settings().POSTGRES_DB)
    else:
        url = 'postgresql+psycopg2://{user}:{psw}@{url}/{db}'.format(
            user=Settings().POSTGRES_USER,
            psw=Settings().POSTGRES_PASSWORD,
            url=f"{Settings().POSTGRES_HOSTNAME}:"
                f"{Settings().POSTGRES_PORT}",
            db=Settings().POSTGRES_DB_TEST)

    return url


@lru_cache()
def get_settings():
    return Settings()
