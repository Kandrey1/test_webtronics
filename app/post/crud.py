from sqlalchemy.orm import Session

from .models import Post
from .. import base_crud


async def get_post(db: Session, post_id: int):
    """
    Возвращает пост.

    :param db: сессия для подключения к БД.
    :param post_id: id поста пользователя.
    """
    return await base_crud.get_record(db=db,
                                      table=Post,
                                      record_id=post_id)


async def get_all_post(db: Session, user_id: int) -> list:
    """
    Возвращает все посты пользователя с user_id.

    :param db: сессия для подключения к БД.
    :param user_id: id пользователя.
    """
    return await base_crud.get_all_record_user(db=db,
                                               table=Post,
                                               filter_id=user_id)


async def create_post(db: Session, data: dict):
    """
    Создает статью пользователя.

    :param db: сессия для подключения к БД.
    :param data: данные нового поста.
    """
    return await base_crud.create_record(db=db,
                                         table=Post,
                                         data=data)


async def update_post(db: Session, post_id: int, data: dict):
    """
    Обновляет данные существующего поста.

    :param db: сессия для подключения к БД.
    :param post_id: id статьи.
    :param data: данные для обновления статьи.
    :return: обновленную статью.
    """
    return await base_crud.update_record(db=db,
                                         table=Post,
                                         record_id=post_id,
                                         data=data)


async def delete_post(db: Session, post_id: int):
    """
    Удаляет пост пользователя.

    :param db: сессия для подключения к БД.
    :param post_id: id статьи.
    """
    return await base_crud.delete_record(db=db,
                                         table=Post,
                                         record_id=post_id)
