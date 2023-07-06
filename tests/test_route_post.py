from starlette import status

from app.post.models import Post
from app.auth.models import User
from tests.conftest import get_test_token


def test_get_post(session, client, create_user_one, create_post_one):
    db = session

    assert db.query(Post).count() == 0
    assert db.query(User).count() == 0
    db.add(create_user_one)
    db.commit()
    db.refresh(create_user_one)
    create_post_one.user_id = create_user_one.id
    db.add(create_post_one)
    db.commit()
    db.refresh(create_post_one)
    assert db.query(Post).count() == 1
    assert db.query(User).count() == 1

    post = db.query(Post).first()
    assert post.title == 'title1'
    assert post.user_id == create_user_one.id

    response = client.get(f"/posts/{create_post_one.id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    access_token = get_test_token(user_id=1)

    header = {"authorization": f"Bearer {access_token}"}
    response = client.get(f"/posts/{create_post_one.id}", headers=header)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['id'] == create_post_one.id
    assert data['text'] == create_post_one.text
    assert data['title'] == create_post_one.title


def test_get_all_post(session, client, create_user_one, create_user_two,
                      create_post_one, create_post_two, create_post_three):
    db = session
    db.add(create_user_one)
    db.add(create_user_two)
    db.commit()
    db.refresh(create_user_one)
    db.refresh(create_user_two)
    assert db.query(Post).count() == 0
    create_post_one.user_id = create_user_one.id
    create_post_two.user_id = create_user_two.id
    create_post_three.user_id = create_user_one.id
    db.add(create_post_one)
    db.add(create_post_two)
    db.add(create_post_three)
    db.commit()
    assert db.query(Post).count() == 3
    # -------
    response = client.get("/posts/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # -------
    access_token = get_test_token(user_id=create_user_one.id)
    header = {"authorization": f"Bearer {access_token}"}
    response = client.get("/posts", headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    # -------
    access_token = get_test_token(user_id=create_user_two.id)

    header = {"authorization": f"Bearer {access_token}"}
    response = client.get("/posts", headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


def test_create_post(session, client, create_user_one, data_post_one,
                     data_post_two, data_post_three):
    db = session
    db.add(create_user_one)
    db.commit()
    assert db.query(Post).count() == 0
    # -------
    res1 = client.post("/posts/")
    assert res1.status_code == status.HTTP_403_FORBIDDEN
    # -------
    access_token = get_test_token(user_id=create_user_one.id)
    header = {"authorization": f"Bearer {access_token}"}
    resp2 = client.post("/posts", json=data_post_one, headers=header)
    data = resp2.json()
    assert resp2.status_code == status.HTTP_201_CREATED
    assert data['title'] == data_post_one['title']
    assert data['text'] == data_post_one['text']

    assert db.query(Post).count() == 1
    client.post("/posts", json=data_post_two, headers=header)
    client.post("/posts", json=data_post_three, headers=header)
    assert db.query(Post).count() == 3


def test_update_post(session, client, create_user_one, create_post_one,
                     data_post_one, data_post_two):
    db = session
    db.add(create_user_one)
    db.commit()
    db.refresh(create_user_one)

    create_post_one.user_id = create_user_one.id
    db.add(create_post_one)
    db.commit()
    db.refresh(create_post_one)
    assert db.query(Post).count() == 1

    post = db.query(Post).first()
    assert post.title == data_post_one['title']
    assert post.text == data_post_one['text']
    # -------
    response = client.put(f"/posts/{create_post_one.id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # -------
    access_token = get_test_token(user_id=create_user_one.id)
    header = {"authorization": f"Bearer {access_token}"}
    response = client.put(f"/posts/{create_post_one.id}",
                          json=data_post_two,
                          headers=header)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data['title'] == data_post_two['title']
    assert data['text'] == data_post_two['text']


def test_delete_post(session, client, create_user_one, create_user_two,
                     create_post_one, create_post_two, create_post_three):
    db = session

    db.add(create_user_one)
    db.add(create_user_two)
    db.commit()
    db.refresh(create_user_one)
    db.refresh(create_user_two)

    assert db.query(Post).count() == 0
    create_post_one.user_id = create_user_one.id
    create_post_two.user_id = create_user_two.id
    create_post_three.user_id = create_user_one.id
    db.add(create_post_one)
    db.add(create_post_two)
    db.add(create_post_three)
    db.commit()
    assert db.query(Post).count() == 3
    # -------
    response = client.delete(f"/posts/{create_post_one.id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # -------
    access_token = get_test_token(user_id=create_user_one.id)
    header = {"authorization": f"Bearer {access_token}"}
    response1 = client.delete(f"/posts/{create_post_one.id}", headers=header)
    assert response1.status_code == status.HTTP_204_NO_CONTENT

    response2 = client.delete(f"/posts/{create_post_two.id}", headers=header)
    assert response2.status_code == status.HTTP_403_FORBIDDEN

    response2 = client.delete("/posts/999999", headers=header)
    assert response2.status_code == status.HTTP_404_NOT_FOUND
