import pytest

from django.contrib.auth import get_user_model
from .factories import UserModelFactory


# 닉네임 중복체크 API
@pytest.mark.django_db
def test_NicknameDuplicationCheckingAPI(client):
    UserModelFactory.create_batch(100)

    url = "/accounts/nickname/"
    response = client.get(url)
    assert response.status_code == 400

    url = "/accounts/nickname/?nickname=testnick"
    response = client.get(url)
    assert response.status_code == 200

    for user in get_user_model().objects.all():
        url = f"/accounts/nickname/?nickname={user.nickname}"
        response = client.get(url)
        assert response.status_code == 412
