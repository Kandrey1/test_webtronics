import datetime

import pytest
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import get_db, Base
from config import get_db_url, Settings
from main import app

from app.auth.models import User
from app.post.models import Post
from app.like.models import LikePost


settings = Settings()
engine = create_engine(
    get_db_url(test=True),
)

TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@event.listens_for(engine, "connect")
def do_connect(dbapi_connection, connection_record):
    dbapi_connection.isolation_level = None


@event.listens_for(engine, "begin")
def do_begin(conn):
    conn.exec_driver_sql("BEGIN")


@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


# ------------------------------ user ------------------------------------------
user_data1 = {
    "username": "user1",
    "email": "email1",
    "password": "pass1"
}

user_data2 = {
    "username": "user2",
    "email": "email2",
    "password": "pass2"
}

fail_user_data1 = {
    "email": "email2",
    "password": "pass2"
}

fail_user_data2 = {
    "username": "user2",
    "email": "email2",
}


@pytest.fixture
def data_user_one():
    return user_data1


@pytest.fixture
def data_user_two():
    return user_data2


@pytest.fixture
def fail_data_user_one():
    return fail_user_data1


@pytest.fixture
def fail_data_user_two():
    return fail_user_data2


@pytest.fixture
def create_user_one():
    return User(**user_data1)


@pytest.fixture
def create_user_two():
    return User(**user_data2)


def get_test_token(user_id: int) -> str:
    now = datetime.datetime.utcnow()
    payload = {'iat': now,
               'nbf': now,
               'exp': now + datetime.timedelta(seconds=settings.JWT_EXPIRES_S),
               'sub': str(user_id)}

    token = jwt.encode(payload,
                       settings.JWT_SECRET_KEY,
                       algorithm=settings.JTW_ALGORITHM)

    return token


# ------------------------------ post ------------------------------------------
post_data1 = {
    "title": "title1",
    "text": "text one",
    "user_id": 1
}

post_data2 = {
    "title": "title2",
    "text": "text two",
    "user_id": 2
}

post_data3 = {
    "title": "title3",
    "text": "text three",
    "user_id": 1
}


@pytest.fixture
def create_post_one():
    return Post(**post_data1)


@pytest.fixture
def create_post_two():
    return Post(**post_data2)


@pytest.fixture
def create_post_three():
    return Post(**post_data3)


@pytest.fixture
def data_post_one():
    return post_data1


@pytest.fixture
def data_post_two():
    return post_data2


@pytest.fixture
def data_post_three():
    return post_data3
