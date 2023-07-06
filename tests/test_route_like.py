from starlette import status

from tests.conftest import get_test_token


def test_set_vote_post(session, client, create_user_one, create_user_two,
                       create_post_one, create_post_two):
    db = session
    db.add(create_user_one)
    db.add(create_user_two)
    db.commit()
    db.refresh(create_user_one)
    db.refresh(create_user_two)

    create_post_one.user_id = create_user_one.id
    create_post_two.user_id = create_user_two.id
    db.add(create_post_one)
    db.add(create_post_two)
    db.commit()
    db.refresh(create_post_one)
    db.refresh(create_post_two)

    data_like1 = {
        "post_id": create_post_one.id,
        "vote": -1
    }
    # -------
    response = client.post("/like/post")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # -------
    access_token = get_test_token(user_id=create_user_one.id)
    header = {"authorization": f"Bearer {access_token}"}
    response = client.post("/like/post", json=data_like1, headers=header)
    data = response.json()
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert data['detail'] == 'Вы не можете голосовать за свои статьи'
    # -------
    data_like2 = {
        "post_id": create_post_two.id,
        "vote": -1
    }
    response = client.post("/like/post", json=data_like2, headers=header)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data['vote'] == -1
    assert data['post_id'] == create_post_two.id

    data_like3 = {
        "post_id": create_post_two.id,
        "vote": 1
    }
    response = client.post("/like/post", json=data_like3, headers=header)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data['vote'] == 1
    assert data['post_id'] == create_post_two.id
