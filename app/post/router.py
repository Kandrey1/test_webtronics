from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from app import security
from . import crud
from .schemas import PostSchema, InputDataPostSchema, UpdateDataPostSchema
from .. import Post
from ..auth.services import get_current_user, check_access
from ..database import get_db
from ..exceptions import RecordNotExistDb, AccessDenied
from logger_app import logger

router = APIRouter(prefix='/posts',
                   tags=['Posts (Статьи)'])


@router.get('/{post_id}', response_model=PostSchema)
async def get_post(post_id: int,
                   db: Session = Depends(get_db),
                   token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Возвращает статью.

    post_id: id статьи.
    # """
    try:
        post = await crud.get_post(db=db, post_id=post_id)

    except RecordNotExistDb:
        raise HTTPException(status_code=404,
                            detail='Такая статья не существует')

    except SQLAlchemyError as e_db:
        logger.error(f'DB: {e_db}')
        raise HTTPException(status_code=500,
                            detail='БД недоступна')

    except Exception as e:
        logger.error(f'Exception: {e}')
        raise HTTPException(status_code=500,
                            detail='Ошибка на сервере, '
                                   'обратитесь к администратору')

    return post


@router.get('/', response_model=List[PostSchema])
async def get_all_post(db: Session = Depends(get_db),
                       token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Возвращает все статьи пользователя.
    """
    try:
        current_user = await get_current_user(db=db, token=token.credentials)

        posts = await crud.get_all_post(db=db, user_id=current_user.id)

    except RecordNotExistDb:
        raise HTTPException(status_code=404,
                            detail='У Вас пока нет статей.')

    except SQLAlchemyError as e_db:
        logger.error(f'DB: {e_db}')
        raise HTTPException(status_code=500, detail='БД недоступна')

    except Exception as e:
        logger.error(f'Exception: {e}')
        raise HTTPException(status_code=500,
                            detail='Ошибка на сервере, '
                                   'обратитесь к администратору')

    return posts


@router.post('/',
             response_model=PostSchema,
             status_code=status.HTTP_201_CREATED)
async def create_post(data: InputDataPostSchema,
                      db: Session = Depends(get_db),
                      token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Создает новую статью.

    """
    try:
        current_user = await get_current_user(db=db, token=token.credentials)

        dct_data = dict(data)
        dct_data.update({"user_id": current_user.id})

        new_post = await crud.create_post(db=db, data=dct_data)

        logger.info(f'Пользователь: "{current_user.id}:{current_user.username}"'
                    f' добавил статью "{new_post.id}:{new_post.title}"')

    except SQLAlchemyError as e_db:
        logger.error(f'DB: {e_db}')
        raise HTTPException(status_code=500, detail='БД недоступна')

    except Exception as e:
        logger.error(f'Exception: {e}')
        raise HTTPException(status_code=500,
                            detail='Ошибка на сервере, '
                                   'обратитесь к администратору')

    return new_post


@router.put('/{post_id}',
            response_model=PostSchema)
async def update_post(up_data: UpdateDataPostSchema,
                      post_id: int,
                      db: Session = Depends(get_db),
                      token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Обновляет статью пользователя.

    post_id: id категории ссылок
    """
    try:
        current_user = await get_current_user(db=db, token=token.credentials)

        dct_data = dict(up_data)
        dct_data.update({"user_id": current_user.id})

        await check_access(db=db,
                           user_id=current_user.id,
                           table=Post,
                           obj_id=post_id)

        up_post = await crud.update_post(db=db,
                                         post_id=post_id,
                                         data=dct_data)
        logger.info(f'Пользователь: "{current_user.id}:{current_user.username}"'
                    f' изменил статью "{up_post.id}:{up_post.title}"')

    except AccessDenied:
        raise HTTPException(status_code=403, detail='Доступ запрещен')

    except RecordNotExistDb:
        raise HTTPException(status_code=404, detail='Такой статьи нет')

    except SQLAlchemyError as e_db:
        logger.error(f'DB: {e_db}')
        raise HTTPException(status_code=500, detail='БД недоступна')

    except Exception as e:
        logger.error(f'Exception: {e}')
        raise HTTPException(status_code=500,
                            detail='Ошибка на сервере, '
                                   'обратитесь к администратору')

    return up_post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int,
                      db: Session = Depends(get_db),
                      token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Удаляет статью пользователя.

    post_id: id поста на удаление.
    """
    try:
        current_user = await get_current_user(db=db, token=token.credentials)

        await check_access(db=db,
                           user_id=current_user.id,
                           table=Post,
                           obj_id=post_id)

        await crud.delete_post(db=db, post_id=post_id)

        logger.info(f'Пользователь: "{current_user.id}:{current_user.username}"'
                    f' удалил статью "{post_id}"')

    except AccessDenied:
        raise HTTPException(status_code=403, detail='Доступ запрещен')

    except RecordNotExistDb:
        raise HTTPException(status_code=404, detail='Такой статьи нет')

    except SQLAlchemyError as e_db:
        logger.error(f'DB: {e_db}')
        raise HTTPException(status_code=500, detail='БД недоступна')

    except Exception as e:
        logger.error(f'Exception: {e}')
        raise HTTPException(status_code=500,
                            detail='Ошибка на сервере, '
                                   'обратитесь к администратору')

    return status.HTTP_204_NO_CONTENT
