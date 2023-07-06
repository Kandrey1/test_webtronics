from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import Base
from .exceptions import RecordNotExistDb


async def get_record(db: Session, table: Base, record_id: int):
    """
    Возвращает одну запись по id.

    :param db: сессия для подключения к БД.
    :param table: имя таблицы для запроса.
    :param record_id: id записи.
    :return: запись из БД.
    """
    try:
        record = db.query(table).filter(table.id == record_id).first()
        if not record:
            raise RecordNotExistDb

    except SQLAlchemyError as e:
        raise e

    return record


async def create_record(db: Session, table: Base, data: dict):
    """
    Создает новую запись в БД.

    :param db: сессия для подключения к БД.
    :param table: имя таблицы для запроса.
    :param data: данные новой записи.
    :return: созданную запись
    """
    try:
        record = table()

        for key, val in data.items():
            setattr(record, key, val)

        db.add(record)
        db.commit()
        db.refresh(record)

    except SQLAlchemyError as e:
        db.rollback()
        raise e

    return record


async def update_record(db: Session, table: Base, record_id: int, data: dict):
    """
    Обновляет существующую запись в БД.

    :param db: сессия для подключения к БД.
    :param table: имя таблицы для запроса.
    :param data: данные новой записи.
    :param record_id:id записи.
    :return: обновленную запись.
    """
    try:
        up_record = await get_record(db=db,
                                     table=table,
                                     record_id=record_id)

        for key, val in data.items():
            setattr(up_record, key, val)

        db.commit()
        db.refresh(up_record)

    except SQLAlchemyError as e:
        db.rollback()
        raise e

    return up_record


async def delete_record(db: Session, table: Base, record_id: int):
    """
    Удаляет запись по id.

    :param db: сессия для подключения к БД.
    :param table: имя таблицы для запроса.
    :param record_id: id записи.
    """
    try:
        record = db.query(table).filter(table.id == record_id).first()
        if not record:
            raise RecordNotExistDb

        db.delete(record)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise e

    return 'status.HTTP_204_NO_CONTENT'


async def get_all_record_user(db: Session, table: Base, filter_id: int):
    """
    Возвращает все записи пользователя(по user_id) из таблицы 'table'.

    :param db: сессия для подключения к БД.
    :param table: имя таблицы для запроса.
    :param filter_id: значение для фильтрации данных.
    :return: запись из БД.
    """
    try:
        records = db.query(table).filter(table.user_id == filter_id).all()

        if not records:
            raise RecordNotExistDb

    except SQLAlchemyError as e:
        raise e

    return records
