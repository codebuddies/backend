import pytest
from django.conf import settings

pytestmark = pytest.mark.django_db

@pytest.mark.skip(reason="App needs rewrite after auth change.")
def test_user_get_absolute_url(user: settings.AUTH_USER_MODEL):
    assert user.get_absolute_url() == f"/users/{user.username}/"
