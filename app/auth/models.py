from sqlalchemy import Column, Integer, String

from ..database import Base


class User(Base):
    """
    Модель данных пользователя.

    email: email адрес пользователя.
    username: имя пользователя(логин)
    password_hash: хэшированный пароль пользователя.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String)
    password = Column(String)
