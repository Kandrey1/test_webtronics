from passlib.context import CryptContext
from starlette import status

from app.auth.models import User


def test_sign_up(session, client, data_user_one, fail_data_user_one,
                 fail_data_user_two):
    db = session

    assert db.query(User).count() == 0

    response = client.post("/auth/sign-up/", json=data_user_one)
    assert db.query(User).count() == 1

    data1 = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data1['token_type'] == "bearer"
    assert type(data1['access_token']) == str

    response = client.post("/auth/sign-up/", json=fail_data_user_one)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.post("/auth/sign-up/", json=fail_data_user_two)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_sign_in(session, client, create_user_one, data_user_one,
                 create_user_two):

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    db = session

    user = create_user_one
    user.password = pwd_context.hash(user.password)
    db.add(user)
    db.commit()

    user = db.query(User).first()
    assert user.username == data_user_one.get('username')
    assert user.email == data_user_one.get('email')

    data_auth = {
        "email": data_user_one.get('email'),
        "password": data_user_one.get('password')
    }

    response = client.post("/auth/sign-in/", json=data_auth)
    data1 = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data1['token_type'] == "bearer"
    assert type(data1['access_token']) == str

    data_auth_fail1 = {
        "email": "er",
        "password": data_user_one.get('password')
    }

    response = client.post("/auth/sign-in/", json=data_auth_fail1)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data_auth_fail2 = {
        "erremail": "er",
        "password": data_user_one.get('password')
    }

    response = client.post("/auth/sign-in/", json=data_auth_fail2)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
