import datetime

from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from config import get_settings
from . import crud
from app.auth.models import User
from app.database import Base
from app.exceptions import RecordNotExistDb, AccessDenied

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

settings = get_settings()


async def get_password_hash(password: str) -> str:
    """
    Возвращает хэшированное значения 'password'.

    :param password: пароль(строка) пользователя
    """
    return pwd_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие введенного пароля и существующий
    хэш пароля пользователя.

    :param plain_password: введенный пароль(строка) для проверки.
    :param hashed_password: хэш существующего пароля.
    :return: True если совпадает, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(user: User) -> str:
    """
    Создает jwt-токен пользователя.
    В токен помещается id пользователя.

    :param user: объект с данными пользователя из таблицы в БД.

    :return: jwt token
    """
    now = datetime.datetime.utcnow()
    payload = {'iat': now,
               'nbf': now,
               'exp': now + datetime.timedelta(seconds=settings.JWT_EXPIRES_S),
               'sub': str(user.id)}

    token = jwt.encode(payload,
                       settings.JWT_SECRET_KEY,
                       algorithm=settings.JTW_ALGORITHM)

    return token


async def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Аутентификация пользователя.

    :param db: сессия для подключения к БД.
    :param email: email пользователя.
    :param password: пароль пользователя.
    :return: объект user если прошел проверку.
    """
    user = await crud.get_user_for_email(db=db, email=email)

    if not user:
        raise RecordNotExistDb

    if not await verify_password(plain_password=password,
                                 hashed_password=user.password):
        raise RecordNotExistDb

    return user


async def get_current_user(db: Session, token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             settings.JWT_SECRET_KEY,
                             algorithms=settings.JTW_ALGORITHM)
        user_id = int(payload.get("sub"))

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await crud.get_user_for_id(db=db, user_id=user_id)

    if user is None:
        raise credentials_exception

    return user


async def check_access(db: Session, user_id: int, table: Base, obj_id: int):
    """
    Проверка доступа на совершения действий пользователя с объектом.

    :param db: сессия для подключения к БД.
    :param user_id: id проверяемого пользователя.
    :param table: Таблица в БД.
    :param obj_id: id объекта(записи в таблице).
    """

    row = db.query(table).filter(table.id == obj_id).first()
    if not row:
        raise RecordNotExistDb

    if not row.user_id == user_id:
        raise AccessDenied
