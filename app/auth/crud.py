from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .models import User
from .services import get_password_hash
from .. import base_crud


async def get_user_for_id(db: Session, user_id: int):
    """
    Возвращает пользователя.

    :param db: сессия для подключения к БД.
    :param user_id: id пользователя.
    """
    return await base_crud.get_record(db=db,
                                      table=User,
                                      record_id=user_id)


async def get_user_for_email(db: Session, email: str):
    """
    Возвращает пользователя.

    :param db: сессия для подключения к БД.
    :param email: email пользователя.
    """
    try:
        user = db.query(User).filter(User.email == email).first()

    except SQLAlchemyError as e:
        raise e

    return user


async def create_user(db: Session, data: dict):
    """
    Создает нового пользователя.

    :param db: сессия для подключения к БД.
    :param data: данные нового пользователя.
    """
    data = {
        "email": data["email"],
        "username": data["username"],
        "password": await get_password_hash(data["password"])
    }
    return await base_crud.create_record(db=db,
                                         table=User,
                                         data=data)
