from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth.schemas import TokenSchema, UserAuthSchema, UserCreateSchema
from . import crud
from .services import create_access_token, authenticate_user
from ..database import get_db
from ..exceptions import RecordNotExistDb, CreateRecordExistDb
from logger_app import logger


router = APIRouter(prefix='/auth',
                   tags=['auth'])


@router.post('/sign-up/', response_model=TokenSchema)
async def sign_up(reg_data: UserCreateSchema,
                  db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.

    Возвращает токен доступа.
    """
    try:
        data = dict(reg_data)

        if await crud.get_user_for_email(db=db, email=data['email']):
            raise CreateRecordExistDb

        user = await crud.create_user(db=db, data=data)

        access_token = await create_access_token(user)

        logger.info(f"Зарегистрирован новый пользователь "
                    f"{user.id}: {user.email} - {user.username}")

    except CreateRecordExistDb:
        raise HTTPException(status_code=404,
                            detail='Пользователь с таким email уже существует.')

    except SQLAlchemyError as e_db:
        logger.error(f'DB: {e_db}')
        raise HTTPException(status_code=500,
                            detail='БД недоступна')

    except Exception as e:
        logger.error(f'Exception: {e}')
        raise HTTPException(status_code=500,
                            detail='Ошибка на сервере, '
                                   'обратитесь к администратору')

    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/sign-in/', response_model=TokenSchema)
async def sign_in(auth_data: UserAuthSchema,
                  db: Session = Depends(get_db)):
    """
    Вход пользователя.

    Возвращает токен доступа.
    """
    try:
        data = dict(auth_data)
        user = await authenticate_user(db=db,
                                       email=data['email'],
                                       password=data['password'])

        access_token = await create_access_token(user)

    except RecordNotExistDb:
        raise HTTPException(status_code=404,
                            detail='Неверный email или пароль.')

    except SQLAlchemyError as e_db:
        logger.error(f'DB: {e_db}')
        raise HTTPException(status_code=500,
                            detail='БД недоступна')

    except Exception as e:
        logger.error(f'Exception: {e}')
        raise HTTPException(status_code=500,
                            detail='Ошибка на сервере, '
                                   'обратитесь к администратору')

    return {"access_token": access_token, "token_type": "bearer"}
