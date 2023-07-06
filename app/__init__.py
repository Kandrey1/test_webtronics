from fastapi import FastAPI
from fastapi.security import HTTPBearer

from app.database import Base, engine

from .auth.models import User
from .post.models import Post
from .like.models import LikePost


def create_app() -> FastAPI:
    app = FastAPI(
        title='Простая социальная сеть.',
        description='Тестовое задание.',
        version='1.0.0',
    )

    Base.metadata.create_all(bind=engine)

    return app


security = HTTPBearer()
